# Imaginary-Notes
**Category:** Web
**Difficulty:** Easy
**Author:** cleverbear57

## Description

I made a new note taking app using Supabase! Its so secure, I put my flag as the password to the "admin" account. I even put my anonymous key somewhere in the site. The password database is called, "users".

## Distribution

- none

## Solution

- If you look into the sources of the website and go to page.js, you can Ctrl-F for "anonkey", and you can find the anonymous key, and the project id. Running curl '"https://<project-id>.supabase.co/rest/v1/users" -H "apikey: <Anonkey>" -H "Authorization: Bearer <Anonkey>"' will give the whole database.
