[![Build Status](https://travis-ci.org/jeschkies/tickets.svg?branch=master)](https://travis-ci.org/jeschkies/tickets)

# tickets
Reboot of a Ticketing System

## Development

Simply call `tox` from the command line to lint and test everything.

For active development you should setup a virtual environment:

```bash
virtualenv devenv
source devenv/bin/activate
pip install -r requirements.txt
pip install -e .
```

You can then run the tests with `pytest`.

The development server is started with `STRIPE_PUBLISHABLE_KEY='...' STRIPE_SECRET_KEY='...' python tickets/tickets.py`.
