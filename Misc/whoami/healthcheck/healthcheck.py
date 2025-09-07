#!/usr/bin/env python3

from pwn import *

try:
  conn = remote("localhost", 1337)
  r = conn.recv()
  assert b"prompt" in r
  exit(0)
except Exception as e:
  print(e)
  exit(1)
