dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer, tests

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --build --dry-run

package-install:
	pip install --user dist/*.whl

coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app

test:
	poetry run pytest tests/