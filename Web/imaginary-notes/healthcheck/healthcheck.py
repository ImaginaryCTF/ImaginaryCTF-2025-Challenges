#!/usr/bin/env python3

import requests

try:
  s = requests.Session()
  r = s.get(f"http://localhost:3000/").text
  exit(0)
except Exception as e:
  print(e)
  exit(1)
