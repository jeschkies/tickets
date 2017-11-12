[![Build Status](https://travis-ci.org/jeschkies/tickets.svg?branch=master)](https://travis-ci.org/jeschkies/tickets) [![Coverage Status](https://coveralls.io/repos/github/jeschkies/tickets/badge.svg)](https://coveralls.io/github/jeschkies/tickets)

# tickets
Reboot of a Ticketing System

## Development

The best way to develop and test this project is with [pipenv](https://docs.pipenv.org/).

Simply install pipenv and the dependencies with `make`.

You can then run the tests with `TICKETFARM_SETTINGS='tickets.config.test' pipenv run pytest`
or everything with `make ci`.

The development server is started with

```bash
FLASK_APP=./tickets/main.py \
STRIPE_PUBLISHABLE_KEY='...' \
STRIPE_SECRET_KEY='...' \
TICKETFARM_SETTINGS='tickets.config.dev' \
pipenv run flask run
```

or simply `STRIPE_PUBLISHABLE_KEY='...' STRIPE_SECRET_KEY='...' make run`.

Migrate any Postgresql database with `DATABASE_URL=postgresql://user:pw@url make
migrate`. The environment variable is also required to run the app in production.

## Deployment

Migrate the database with

```
DATABASE_URL=postgresql://user:pw@url make migrate
```

and deploy the newest version to heroku with

```
make deploy
```
