init:
	python3.11 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt; pre-commit install
	. venv/bin/activate; cd src/fastapi_app; poetry install
	. venv/bin/activate; cd src/streamlit_app; poetry install
	@echo "\n\033[0;32mYour dev environment is ready!\033[0m\n"

test:
	. venv/bin/activate; cd src/; PYTHONPATH=. pytest tests -W ignore::DeprecationWarning

docker-run:
	docker-compose up --build

format:
	( \
		. venv/bin/activate; cd src;\
		isort streamlit_app; \
		black fastapi_app; \
		isort tests; \
		black tests; \
	)

lint-check:
	. venv/bin/activate; cd src; flake8 streamlit_app; flake8 fastapi_app; \
	pylint streamlit_app; refurb --enable-all streamlit_app; \
	pylint fastapi_app; refurb --enable-all fastapi_app; \
	flake8 tests;
