init:
	pip install pipenv
	pipenv install --dev

ci:
	pipenv run flake8 tickets tests
	pipenv run yapf -irp tickets tests
	pipenv run alembic -n test upgrade head
	TICKETFARM_SETTINGS='tickets.config.test' pipenv run pytest

run:
	pipenv run alembic -n dev upgrade head
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py pipenv run flask run

debug:
	pipenv run alembic -n dev upgrade head
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py FLASK_DEBUG=1 pipenv run flask run

clean:
	rm -f test.db
