init:
	pip3 install pipenv
	pipenv install --dev --skip-lock

test:
	pipenv run yapf -irp tickets tests migrations
	pipenv run flake8 tickets tests
	pipenv run alembic -n test upgrade head
	TICKETFARM_SETTINGS='tickets.config.test' pipenv run pytest --cov-config .coveragerc --cov tickets --cov-report term

migrate:
	pipenv run alembic -n prod upgrade head

deploy:
	git push heroku master

serve:
	pipenv run alembic -n dev upgrade head
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py FLASK_DEBUG=1 pipenv run flask run

clean:
	rm -f test.db
