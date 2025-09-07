#!/usr/bin/env python3

import requests

try:
  s = requests.Session()
  r = s.get(f"http://localhost:80/").text
  if "Tax Return" in r:
    exit(0)
  else:
    print(r)
    exit(1)
except Exception as e:
  print(e)
  exit(1)
