import os
import json
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, join_room, emit
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(16))

socketio = SocketIO(app)

# Secret prefix used to identify bot passwords; generated at startup
BOT_SECRET_PREFIX = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

PROFILES_DIR = 'profiles'
if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

games = {}
# Directory for language wordlists
WORDS_DIR = 'words'
# Ensure the words directory exists
if not os.path.exists(WORDS_DIR):
    os.makedirs(WORDS_DIR)
# Available languages (filenames without extension)
LANGUAGES = [os.path.splitext(f)[0] for f in sorted(os.listdir(WORDS_DIR)) if f.lower().endswith('.txt')]

def load_profile(username):
    path = os.path.join(PROFILES_DIR, username)
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return json.load(f)

def save_profile(profile):
    path = os.path.join(PROFILES_DIR, profile['username'])
    with open(path, 'w') as f:
        json.dump(profile, f)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('lobby'))
        return render_template('register.html')
    # get form inputs
    username = request.form.get('username', '').strip().replace('/', '')
    raw_pass = request.form.get('password', '')
    if len(raw_pass) < 8:
        flash('Password must be at least 8 characters')
        return redirect(url_for('register'))
    if not username or not raw_pass:
        flash('Username and password required')
        return redirect(url_for('register'))
    if load_profile(username):
        flash('Username already exists')
        return redirect(url_for('register'))
    # detect bot via secret prefix in password
    is_bot = False
    pwd = raw_pass
    if raw_pass.startswith(BOT_SECRET_PREFIX):
        is_bot = True
        pwd = raw_pass[len(BOT_SECRET_PREFIX):]
    # hash stripped password
    pw_hash = generate_password_hash(pwd)
    profile = {'username': username, 'password_hash': pw_hash, 'wins': 0, 'is_bot': is_bot}
    save_profile(profile)
    session['username'] = username
    session['is_bot'] = is_bot
    return redirect(url_for('lobby'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('lobby'))
        return render_template('login.html')
    username = request.form.get('username', '').strip()
    raw_pass = request.form.get('password', '')
    profile = load_profile(username)
    if not profile:
        flash('Invalid username or password')
        return redirect(url_for('login'))
    # detect bot via secret prefix and strip
    is_bot = False
    pwd = raw_pass
    if raw_pass.startswith(BOT_SECRET_PREFIX):
        is_bot = True
        pwd = raw_pass[len(BOT_SECRET_PREFIX):]
    # verify password
    if not check_password_hash(profile['password_hash'], pwd):
        flash('Invalid username or password')
        return redirect(url_for('login'))
    session['username'] = username
    # preserve bot flag from profile or prefix
    session['is_bot'] = profile.get('is_bot', is_bot)
    return redirect(url_for('lobby'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lobby')
def lobby():
    if 'username' not in session:
        return redirect(url_for('index'))
    profile = load_profile(session['username'])
    wins = profile.get('wins', 0) if profile else 0
    return render_template('lobby.html', wins=wins, languages=LANGUAGES)

@app.route('/create_game', methods=['POST'])
def create_game():
    if 'username' not in session:
        return redirect(url_for('index'))
    # generate unique code
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if code not in games:
            break
    # prepare game with selected language word list
    # determine language (default to first available)
    language = request.form.get('language', None)
    if not language or '.' in language:
        language = LANGUAGES[0] if LANGUAGES else None
    # load words for this language
    word_list = []
    if language:
        wl_path = os.path.join(WORDS_DIR, f"{language}.txt")
        try:
            with open(wl_path) as wf:
                word_list = [line.strip() for line in wf if line.strip()]
        except IOError as e:
            print(e)
            word_list = []
    # fallback if needed
    if not word_list:
        word_list = []
    # pick 25 random words
    words = random.sample(word_list, 25) if len(word_list) >= 25 else random.sample(word_list * 25, 25)
    start_team = random.choice(['red', 'blue'])
    counts = {
        'red': 9 if start_team == 'red' else 8,
        'blue': 9 if start_team == 'blue' else 8
    }
    # assign colors by index to support duplicate words
    indices = list(range(25))
    random.shuffle(indices)
    colors_list = [None] * 25
    # one assassin
    assassin_idx = indices.pop()
    colors_list[assassin_idx] = 'assassin'
    # team words
    for team in ['red', 'blue']:
        for _ in range(counts[team]):
            idx = indices.pop()
            colors_list[idx] = team
    # the rest are neutral
    for idx in indices:
        colors_list[idx] = 'neutral'
    # determine hard mode (double win points)
    hard_mode = bool(request.form.get('hard_mode'))
    # initialize game state
    game = {
        'players': [session['username']],
        'board': words,
        'colors': colors_list,
        'revealed': [False] * 25,
        'start_team': start_team,
        'team_color': start_team,
        'clue_giver': None,
        'clue': None,
        'guesses_remaining': 0,
        'score': 0,
        'hard_mode': hard_mode,
        'bots': []
    }
    games[code] = game
    return redirect(url_for('game_view', code=code))

@app.route('/join_game', methods=['POST'])
def join_game():
    if 'username' not in session:
        return redirect(url_for('index'))
    code = request.form.get('code', '').strip().upper()
    game = games.get(code)
    if not game or len(game['players']) >= 2:
        flash('Invalid or full game code')
        return redirect(url_for('lobby'))
    if session['username'] in game['players']:
        return redirect(url_for('game_view', code=code))
    game['players'].append(session['username'])
    # assign the joiner as clue giver
    game['clue_giver'] = session['username']
    return redirect(url_for('game_view', code=code))

@app.route('/game/<code>')
def game_view(code):
    if 'username' not in session:
        return redirect(url_for('index'))
    game = games.get(code)
    if not game or session['username'] not in game['players']:
        flash('Invalid game access')
        return redirect(url_for('lobby'))
    player_idx = game['players'].index(session['username'])
    return render_template('game.html', code=code, username=session['username'], player_idx=player_idx)

@app.route('/add_bot', methods=['POST'])
def add_bot():
    if 'username' not in session:
        return redirect(url_for('index'))
    code = request.form.get('code', '').strip().upper()
    game = games.get(code)
    if not game or session['username'] not in game['players']:
        flash('Invalid game code')
        return redirect(url_for('lobby'))
    # spawn a bot process to join this game
    import subprocess, sys, os as _os
    script = _os.path.join(_os.getcwd(), 'bot.py')
    # pass secret prefix to bot via environment
    env = _os.environ.copy()
    env['BOT_SECRET_PREFIX'] = BOT_SECRET_PREFIX
    subprocess.Popen([sys.executable, script, code], env=env)
    return redirect(url_for('game_view', code=code))

@socketio.on('join')
def on_join():
    code = request.args.get('code')
    game = games.get(code)
    username = session.get('username')
    if not game or username not in game['players']:
        return
    # join the game room and record this client's socket id
    join_room(code)
    # map this player's username to their session id for personalized emits
    game.setdefault('sids', {})[username] = request.sid
    # record bot participants
    if session.get('is_bot'):
        if 'bots' in game and username not in game['bots']:
            game['bots'].append(username)
    # when both players have joined via WebSocket, send start_game to each individually
    # ensure game has two players and both have connected
    if len(game.get('players', [])) == 2 and len(game.get('sids', {})) == 2:
        # common payload for both roles
        payload_common = {
            'board': game['board'],
            'revealed': game['revealed'],
            'clue_giver': game['clue_giver'],
            'team_color': game['team_color'],
            'score': game['score'],
            'clue': game['clue'],
            'guesses_remaining': game['guesses_remaining'],
            'hard_mode': game.get('hard_mode', False)
        }
        # send full colors to clue giver, omit for guesser
        for player, sid in game['sids'].items():
            data = payload_common.copy()
            if player == game['clue_giver']:
                data['colors'] = game['colors']
            emit('start_game', data, room=sid)

@socketio.on('give_clue')
def on_give_clue(data):
    code = request.args.get('code')
    game = games.get(code)
    user = session.get('username')
    # only clue giver can send clues
    if not game or user != game.get('clue_giver'):
        return
    clue = data.get('clue')
    try:
        num = int(data.get('number', 0))
    except:
        num = 0
    game['clue'] = clue
    game['guesses_remaining'] = num
    emit('clue_given', {'clue': clue, 'guesses_remaining': num}, room=code)

@socketio.on('make_guess')
def on_make_guess(data):
    code = request.args.get('code')
    game = games.get(code)
    user = session.get('username')
    # only guesser and when guesses remain
    if not game or user == game.get('clue_giver') or game.get('guesses_remaining', 0) <= 0:
        return
    # extract index of guessed cell
    try:
        idx = int(data.get('index'))
    except:
        return
    # validate index and reveal state
    if idx < 0 or idx >= len(game['board']) or game['revealed'][idx]:
        return
    word = game['board'][idx]
    color = game['colors'][idx]
    game['revealed'][idx] = True
    # scoring: +1 for your team, -1 for opponent, 0 for neutral
    team = game.get('team_color')
    if color == team:
        game['score'] += 1
    elif color != 'neutral':
        game['score'] -= 1
    # decrement guesses
    game['guesses_remaining'] -= 1
    # check lose condition: assassin, negative score, or opponent pick in hard mode
    opponent = 'red' if team == 'blue' else 'blue'
    hard_mode = game.get('hard_mode', False)
    lose_flag = (color == 'assassin' or game['score'] < 0 or (hard_mode and color == opponent))
    if lose_flag:
        # determine lose message
        if hard_mode and color == opponent:
            lose_msg = "Sorry, in Hard Mode you guessed the opposing team's word. You lost!"
        elif color == 'assassin':
            lose_msg = "Sorry, you hit the assassin. You lost!"
        elif game['score'] < 0:
            lose_msg = "Sorry, your score went negative. You lost!"
        else:
            lose_msg = "Sorry, you lost!"
        emit('update', {
            'index': idx,
            'color': color,
            'score': game['score'],
            'guesses_remaining': game['guesses_remaining'],
            'lose': True,
            'lose_msg': lose_msg
        }, room=code)
        return
    # check win condition: all your team words revealed
    win_flag = all(game['revealed'][i] for i, col in enumerate(game['colors']) if col == team)
    if win_flag:
        # award wins (double if hard mode)
        bonus = 2 if game.get('hard_mode') else 1
        for p in game['players']:
            profile = load_profile(p)
            if profile:
                profile['wins'] = profile.get('wins', 0) + bonus
                save_profile(profile)
        # prepare payload, including flag if bot is in game and hard mode
        payload = {
            'index': idx,
            'color': color,
            'score': game['score'],
            'guesses_remaining': game['guesses_remaining'],
            'win': True,
            'wins_awarded': bonus
        }
        # cooperative bot wins when human wins
        if game.get('hard_mode'):
            # include flag if a bot is in this game
            if game.get('bots'):
                try:
                    payload['flag'] = os.environ.get("FLAG_2")
                except Exception:
                    pass
        emit('update', payload, room=code)
        return
    # normal update
    emit('update', {
        'index': idx,
        'color': color,
        'score': game['score'],
        'guesses_remaining': game['guesses_remaining'],
        'win': False
    }, room=code)

if __name__ == '__main__':
    socketio.run(app)
