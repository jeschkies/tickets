[![Build Status](https://travis-ci.org/jeschkies/tickets.svg?branch=master)](https://travis-ci.org/jeschkies/tickets) [![Coverage Status](https://coveralls.io/repos/github/jeschkies/tickets/badge.svg?branch=master&service=github)](https://coveralls.io/github/jeschkies/tickets)

# tickets
Reboot of a Ticketing System

## Development

The best way to develop and test this project is with [pipenv](https://docs.pipenv.org/).

Simply install pipenv and the dependencies with `make`.

You can then run the tests with `TICKETFARM_SETTINGS='tickets.config.test' pipenv run pytest`
or everything with `make test`.

The development server is started with

```bash
FLASK_APP=./tickets/main.py \
STRIPE_PUBLISHABLE_KEY='...' \
STRIPE_SECRET_KEY='...' \
TICKETFARM_SETTINGS='tickets.config.dev' \
pipenv run flask run
```

or simply `STRIPE_PUBLISHABLE_KEY='...' STRIPE_SECRET_KEY='...' make serve`.

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

## Configuration

The app takes the following environment variables

* `SENTRY_DSN` for configuring the connection to sentry. This can be empty for
    tests.
* `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` for Stripe payments.
* `DATABASE_URL` for configuring the PostgreSQL database connection.
* `TICKETFARM_SETTINGS` should to a module in `tickets.config`.

The migrations configuration in `alembic.ini` includes the following targets

* `prod` for migrating the production PostgreSQL database.
* `dev` for migrating a development SQLite database.
* `test` for migrating the test SQLite database `test.db`.

Further app related configuration can be found in `tickets/config/default.py`.
