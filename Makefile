.EXPORT_ALL_VARIABLES:
.PHONY: parse db-clean db-init up up-dev test

FLASK_APP=hivery
FLASK_ENV=production

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
	FLASK_ENV=development
	flask run

test:
	FLASK_ENV=testing
	python -m pytest
