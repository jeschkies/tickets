init:
	pip install pipenv
	pipenv install --dev

ci:
	pipenv run yapf -irp tickets tests
	pipenv run flake8 tickets tests
	TICKETFARM_SETTINGS='tickets.config.test' pipenv run pytest --cov tickets --cov-report term

run:
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py pipenv run flask run

debug:
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py FLASK_DEBUG=1 pipenv run flask run
