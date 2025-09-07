import socket, select, base64, random, string, os, threading
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

HOST = "0.0.0.0"
PORT = 8080

routes = {}
accounts = {}

FLAG_FILE = "./flag.txt"

admin_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
accounts["admin"] = admin_password
print(f"[+] Admin password: {admin_password}")

def route(path):
    """Register route"""
    def decorator(func):
        routes[path] = func
        return func
    return decorator

def build_response(body, status=200, headers=None, keep_alive=True):
    status_line = f"HTTP/1.1 {status} {'OK' if status==200 else 'ERROR'}"
    default_headers = {
        "Content-Type": "text/html",
        "Content-Length": str(len(body)),
        "Server": "pwnserver/1.0",
        "Connection": "keep-alive" if keep_alive else "close"
    }
    if headers:
        default_headers.update(headers)
    header_lines = [f"{k}: {v}" for k,v in default_headers.items()]
    return "\r\n".join([status_line]+header_lines+["",""])+body

# home
@route("/")
def index(method, body, query=None, headers=None, client_addr=None):
    with open("files/index.html", "r") as f:
        return build_response(f.read())

# flag route for admin
@route("/flag")
def flag_route(method, body, query=None, headers=None, client_addr=None):
    if 'authorization' not in headers:
        return build_response("Missing Authorization header", status=401, headers={"WWW-Authenticate": 'Basic realm="Login Required"'})

    auth = headers['authorization']
    if not auth.startswith("Basic "):
        return build_response("Invalid Authorization method", status=401, headers={"WWW-Authenticate": 'Basic realm="Login Required"'})

    try:
        encoded = auth.split()[1]
        decoded = base64.b64decode(encoded).decode()
        username, password = decoded.split(":",1)
    except Exception as e:
        print(e)
        return build_response("Malformed Authorization header", status=401, headers={"WWW-Authenticate": 'Basic realm="Login Required"'})

    if accounts.get(username) == password and username == "admin":
        if os.path.exists(FLAG_FILE):
            with open(FLAG_FILE, "r") as f:
                flag_content = f.read()
            return build_response(f"<pre>{flag_content}</pre>")
        else:
            return build_response("<h1>Flag file not found</h1>", status=404)
    else:
        return build_response("Unauthorized", status=401, headers={"WWW-Authenticate": 'Basic realm="Login Required"'})

# internal register route
@route("/register")
def register_route(method, body, query=None, headers=None, client_addr=None):
    if method.upper() != "POST":
        return build_response("Method not allowed", status=405)

    if client_addr[0] != "127.0.0.1":
        return build_response("Access denied", status=401)

    username = headers.get("x-username")
    password = headers.get("x-password")

    if not username or not password:
        return build_response("Missing X-Username or X-Password header", status=400)

    accounts[username] = password
    return build_response(f"User '{username}' registered successfully!")

@route("/visit")
def visit_route(method, body, query=None, headers=None, client_addr=None):
    if method.upper() != "POST":
        return build_response("Method not allowed", status=405)

    target = headers.get("x-target")
    if not target:
        return build_response("Missing X-Target header", status=400)

    def visit_site(url):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print(f"[+] Selenium visited {url}")
        except Exception as e:
            print(f"[!] Error visiting {url}: {e}")
        finally:
            driver.quit()

    threading.Thread(target=visit_site, args=(target,), daemon=True).start()
    return build_response(f"Spawning Selenium bot to visit: {target}")

# server logic
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)
print(f"[*] Listening on {HOST}:{PORT}")

clients = {}

while True:
    read_list = [server]+list(clients.keys())
    rlist, _, _ = select.select(read_list, [], [], 0.1)

    for s in rlist:
        if s is server:
            client_sock, addr = server.accept()
            client_sock.setblocking(False)
            clients[client_sock] = {"addr": addr, "buffer": b""}
            print(f"[*] New client {addr}")
        else:
            client = clients[s]
            try:
                data = s.recv(4096)
                if not data:
                    s.close()
                    del clients[s]
                    continue

                client["buffer"] += data

                while True:
                    request_text = client["buffer"].decode(errors="ignore")
                    if "\r\n\r\n" not in request_text:
                        break

                    header, _, body = request_text.partition("\r\n\r\n")
                    lines = header.splitlines()
                    if not lines:
                        client["buffer"] = b""
                        break

                    try:
                        method, path_query, http_version = lines[0].split()
                        parsed = urlparse(path_query)
                        path = parsed.path
                        query = parse_qs(parsed.query)
                    except:
                        s.send(build_response("400 Bad Request", status=400).encode())
                        s.close()
                        del clients[s]
                        break

                    content_length = 0
                    keep_alive = http_version.upper()=="HTTP/1.1"
                    headers = {}
                    for line in lines[1:]:
                        headers[line.lower().split(": ")[0]] = ": ".join(line.split(": ")[1:])
                        if line.lower().startswith("content-length:"):
                            content_length = int(line.split(":",1)[1].strip())
                        if line.lower().startswith("connection:"):
                            if "close" in line.lower(): keep_alive=False
                            elif "keep-alive" in line.lower(): keep_alive=True

                    post_body = body[:content_length] if method.upper()=="POST" else ""

                    handler = routes.get(path)
                    if handler:
                        response_body = handler(method, post_body, query, headers, addr)
                    else:
                        response_body = build_response("<h1>404 Not Found</h1>", status=404, keep_alive=keep_alive)

                    s.send(response_body.encode())
                    client["buffer"] = client["buffer"][len(header)+4+content_length:]

                    if not keep_alive:
                        s.close()
                        del clients[s]
                        break

            except Exception as e:
                print(f"[!] Error with client {client['addr']}: {e}")
                s.close()
                del clients[s]
