dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --build --dry-run

package-install:
	pip install --user dist/*.whl

coverage:
	poetry run pytest --cov=tests/ --cov-report xml

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
