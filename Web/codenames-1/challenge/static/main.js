document.addEventListener('DOMContentLoaded', function() {
  var socket = io({ query: 'code=' + code });
  var waitingDiv = document.getElementById('waiting');
  var scoreDiv = document.getElementById('score');
  var scoreVal = document.getElementById('score_val');
  var clueInput = document.getElementById('clue_input');
  var clueWord = document.getElementById('clue_word');
  var clueNum = document.getElementById('clue_num');
  var sendClueBtn = document.getElementById('send_clue');
  var clueDisplay = document.getElementById('clue_display');
  var clueText = document.getElementById('clue_text');
  var guessesVal = document.getElementById('guesses_val');
  var boardTable = document.getElementById('board');
  // display your team color
  var colorDiv = document.getElementById('your_color');
  var colorVal = document.getElementById('team_color_val');
  var textMap = { red: '#c00', blue: '#00c' };
  // color maps for board
  var lightMap = { red: '#ff9999', blue: '#9999ff', neutral: '#dddddd', assassin: '#777777' };
  var darkMap  = { red: '#cc6666', blue: '#6666cc', neutral: '#bbbbbb', assassin: '#333333' };
  var boardColors, isClueGiver;
  socket.on('connect', function() {
    socket.emit('join');
  });
  socket.on('start_game', function(data) {
    window.board = data.board;
    window.revealed = data.revealed;
    window.clue_giver = data.clue_giver;
    window.team_color = data.team_color;
    window.score = data.score;
    waitingDiv.style.display = 'none';
    scoreDiv.style.display = 'block';
    scoreVal.innerText = window.score;
    // show your team color
    colorDiv.style.display = 'block';
    var team = data.team_color;
    var teamText = team.charAt(0).toUpperCase() + team.slice(1);
    colorVal.innerText = teamText;
    colorVal.style.color = textMap[team] || team;
    // indicate hard mode if enabled
    var hardLabel = document.getElementById('hard_mode_label');
    if (hardLabel) {
      hardLabel.style.display = data.hard_mode ? 'inline' : 'none';
    }
    // prepare board colors and role
    isClueGiver = (username === data.clue_giver);
    // only clue giver receives the full color mapping initially
    boardColors = isClueGiver ? data.colors : [];
    renderBoard();
    if (isClueGiver) {
      clueInput.style.display = 'block';
      clueDisplay.style.display = 'none';
    } else {
      clueInput.style.display = 'none';
      clueDisplay.style.display = 'block';
      clueText.innerText = 'Waiting for clue';
      guessesVal.innerText = '';
    }
    boardTable.style.display = 'table';
  });
  socket.on('clue_given', function(data) {
    var clue = data.clue;
    var guesses = data.guesses_remaining;
    clueDisplay.style.display = 'block';
    clueText.innerText = clue;
    guessesVal.innerText = guesses;
    if (username === window.clue_giver) {
      clueInput.style.display = 'none';
    }
    renderBoard();
  });
  socket.on('update', function(data) {
    var idx = data.index;
    var color = data.color;
    window.revealed[idx] = true;
    colorCell(idx, color);
    window.score = data.score;
    var rem = data.guesses_remaining;
    scoreVal.innerText = window.score;
    guessesVal.innerText = rem;
    // handle lose
    if (data.lose) {
      var msg = data.lose_msg || 'Sorry, you lost!';
      alert(msg);
      window.location.href = '/lobby';
      return;
    }
    // handle win
    if (data.win) {
      // detect hard mode victory by double win award
      var award = data.wins_awarded || 1;
      if (award === 2) {
        alert('Congratulations! Hard Mode victory! You earned 2 wins!');
      } else {
        alert('Congratulations! You won!');
      }
      if (data.flag) {
        alert('Flag: ' + data.flag);
      }
      window.location.href = '/lobby';
      return;
    }
    if (rem <= 0) {
      if (username === window.clue_giver) {
        clueInput.style.display = 'block';
      }
    }
  });
  sendClueBtn.addEventListener('click', function() {
    var clue = clueWord.value.trim();
    var num = parseInt(clueNum.value, 10);
    if (!clue || isNaN(num) || num < 1) { return; }
    socket.emit('give_clue', { clue: clue, number: num });
  });
  function renderBoard() {
    boardTable.innerHTML = '';
    for (var i = 0; i < board.length; i++) {
      if (i % 5 === 0) {
        var row = boardTable.insertRow();
      }
      var word = board[i];
      var cell = row.insertCell();
      cell.innerHTML = word;
      cell.id = 'cell-' + i;
      cell.setAttribute('data-idx', i);
      cell.className = 'cell';
      if (isClueGiver) {
        // show all colors, darker for guessed
        var base = lightMap[boardColors[i]];
        cell.style.backgroundColor = base;
        if (revealed[i]) {
          cell.style.backgroundColor = darkMap[boardColors[i]];
          cell.style.border = '2px solid #000';
        }
      } else {
        // only show guessed colors; unrevealed entries stay white
        if (revealed[i]) {
          cell.style.backgroundColor = lightMap[boardColors[i]];
        } else {
          cell.style.backgroundColor = '#ffffff';
        }
        cell.addEventListener('click', function() {
          var idx = parseInt(this.getAttribute('data-idx'), 10);
          if (revealed[idx] || parseInt(guessesVal.innerText, 10) <= 0) { return; }
          socket.emit('make_guess', { index: idx });
        });
      }
    }
  }
  function colorCell(idx, color) {
    var cell = document.getElementById('cell-' + idx);
    if (isClueGiver) {
      cell.style.backgroundColor = darkMap[boardColors[idx]];
      cell.style.border = '2px solid #000';
    } else {
      // apply light-colored reveal for guesser and record it
      cell.style.backgroundColor = lightMap[color] || '#ffffff';
      boardColors[idx] = color;
    }
  }
});
