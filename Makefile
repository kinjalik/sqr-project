init:
	python3.11 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt; pre-commit install
	. venv/bin/activate; cd src/; poetry install
	@echo "\n\033[0;32mYour dev environment is ready!\033[0m\n"

docker-run:
	docker build . -t sqr-project
	docker run -p 8080:8080 --rm -ti sqr-project

test:
	. venv/bin/activate; cd src/; PYTHONPATH=. pytest tests -W ignore::DeprecationWarning

format:
	( \
		. venv/bin/activate; cd src;\
		isort app; isort tests; \
		black app; black tests; \
	)

lint-check:
	. venv/bin/activate; cd src; flake8 app; flake8 tests; pylint app; refurb --enable-all app
