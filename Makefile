init:
	pip install pipenv
	pipenv install --dev

ci:
	pipenv run flake8 tickets tests
	pipenv run yapf -irp tickets tests
	TICKETFARM_SETTINGS='tickets.config.test' pipenv run pytest

run:
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py pipenv run flask run

debug:
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py FLASK_DEBUG=1 pipenv run flask run
