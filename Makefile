define USAGE
🎫  Ticketfarm hand-crafted build system ⚙️

Commands:
  init      Install Python dependencies with pipenv
  test      Run linters, test db migrations and tests.
  migrate   Run db migrations for production.
  deploy    Deploy to heroku.
  serve     Run app in dev environment.
  fixtures  Populate dev db with fixtures data.
  clean     Remove test db.
endef

export USAGE
help:
	@echo "$$USAGE"

init:
	pip3 install pipenv
	pipenv install --dev --skip-lock

test:
	pipenv run yapf -irp tickets tests migrations
	pipenv run flake8 --max-line-length=100 tickets tests
	pipenv run alembic -n test upgrade head
	TICKETFARM_SETTINGS='tickets.config.test' pipenv run pytest --cov-config .coveragerc --cov tickets --cov-report term

migrate:
	pipenv run alembic -n prod upgrade head

deploy:
	git push heroku master

serve:
	pipenv run alembic -n dev upgrade head
	TICKETFARM_SETTINGS='tickets.config.dev' FLASK_APP=./tickets/main.py FLASK_DEBUG=1 pipenv run flask run

fixtures:
	pipenv run alembic -n dev upgrade head
	pipenv run python tests/fixtures/dev.py

clean:
	rm -f test.db
