# nightcore
**Category:** Forensics
**Difficulty:** Medium
**Author:** Minerva-007.

## Description

Squidward made an important internet announcement at some point in history. Can you find out the timestamp for when he said that?
The flag format is `ictf{12345678}` where `12345678` is the POSIX timestamp.
By the way, Bikini Bottoms run at 50Hz mains.

## Distribution

- `nightcore.mp3`

## Solution

Upon a single sided FFT, a peak is found at 49.3757Hz. Checking in the grid frequency database, the corresponding timestamp is 1731128930.