'use strict'

const bcrypt = require('bcrypt');
const sqlite3 = require('sqlite3').verbose()
const db = new sqlite3.Database(':memory:')
const normalizeEmail = require('normalize-email')
const crypto = require('crypto')
const path = require('path')
const express = require('express')
const session = require('express-session');
const rateLimit = require('express-rate-limit');


db.serialize(() => {
    db.run('CREATE TABLE users (email TEXT UNIQUE, password TEXT)')
})

const limiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    limit: 10,
    standardHeaders: 'draft-8',
    legacyHeaders: false,
    handler: (req, res) => res.render('limited')
})

const app = express()

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.urlencoded())

app.use(session({
    resave: false,
    saveUninitialized: false,
    secret: crypto.randomBytes(64).toString('hex')
}));

app.use((req, res, next) => {
    var err = req.session.error;
    var msg = req.session.message;
    delete req.session.error;
    delete req.session.message;
    res.locals.err = '';
    res.locals.msg = '';
    res.locals.user = '';
    if (err) res.locals.err = err;
    if (msg) res.locals.msg = msg;
    if (req.session.user) res.locals.user = req.session.user.email.split("@")[0]
    next();
});

function restrict(req, res, next) {
    if (req.session.user) {
        next();
    } else {
        req.session.error = 'You need to be logged in to view this page'
        res.redirect('/login');
    }
}

function authenticated(req, res, next) {
    if (req.session.user) {
        res.redirect('/dashboard');
    } else {
        next();
    }
}

function authenticate(email, password, fn) {
    db.get(`SELECT * FROM users WHERE email = ?`, [email], (err, user) => {
        if (err) return fn(err, null)
        if (user && bcrypt.compareSync(password, user.password)) {
            return fn(null, user)
        } else {
            return fn(null, null)
        }
    });
}

app.post('/session', limiter, (req, res, next) => {
    if (!req.body) return res.redirect('/login')

    const email = normalizeEmail(req.body.email)
    const password = req.body.password

    authenticate(email, password, (err, user) => {
        if (err) return next(err)
        if (user) {
            req.session.regenerate(() => {
                req.session.user = user;
                res.redirect('/dashboard');
            });
        } else {
            req.session.error = 'Failed to log in'
            res.redirect('/login');
        }
    })
})

app.post('/user', limiter, (req, res, next) => {
    if (!req.body) return res.redirect('/login')

    const nEmail = normalizeEmail(req.body.email)

    if (nEmail.length > 64) {
        req.session.error = 'Your email address is too long'
        return res.redirect('/login')
    }

    const initialPassword = req.body.email + crypto.randomBytes(16).toString('hex')
    bcrypt.hash(initialPassword, 10, function (err, hash) {
        if (err) return next(err)

        const query = "INSERT INTO users VALUES (?, ?)"
        db.run(query, [nEmail, hash], (err) => {
            if (err) {
                if (err.code === 'SQLITE_CONSTRAINT') {
                    req.session.error = 'This email address is already registered'
                    return res.redirect('/login')
                }
                return next(err)
            }

            // TODO: Send email with initial password

            req.session.message = 'An email has been sent with a temporary password for you to log in'
            res.redirect('/login')
        })
    })
})

app.get('/register', authenticated, (req, res) => {
    res.render('register');
});

app.get('/login', authenticated, (req, res) => {
    res.render('login');
});

app.get('/logout', (req, res) => {
    req.session.destroy(function () {
        res.redirect('/login');
    });
});

app.get('/dashboard', restrict, (req, res) => {
    res.render('dashboard');
});

app.get('/', (req, res) => res.redirect('/dashboard'))

const port = 3000
app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})
