# passwordless

**Category:** Web
**Difficulty:** Easy
**Author:** Ciaran

## Description

Didn't have time to implement the email sending feature but that's ok, the site is 100% secure if nobody knows their password to sign in!

## Distribution

TBC (Everything in challenge directory can be distributed)

## Solution

Bcrypt hashed secrets have a length limit of 72 chars, given a sufficiently long email address the random secret appended won't be included in the hash.
To bypass the length check can abuse the email normalisation (more details on the [normalise-email](https://www.npmjs.com/package/normalize-email) package) for example providing a gmail address like `test+678901234567890123456789012345678901234567890123456789012@gmail.com` which is 72 characters long.

Register using such an email address, then provide the same email as the password when logging in.
