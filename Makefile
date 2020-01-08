.EXPORT_ALL_VARIABLES:
.PHONY: requirements parse db-clean db-init up up-dev test

FLASK_APP=hivery
FLASK_ENV=production

requirements:
	pip install wheel
	pip install -r requirements.txt

parse:
	python scripts/parse.py resources

db-clean:
	@echo Removing database file if it exists
	rm -f hivery/hivery.db

db-init: db-clean
	@echo Building database from resources directory files
	flask db-init

up:
	flask run

up-dev:
	$(eval FLASK_ENV=development)
	flask run

test:
	$(eval FLASK_ENV=testing)
	python -m pytest

api_features:
	python scripts/api_features.py
