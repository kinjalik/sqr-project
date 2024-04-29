ifdef SILENT
.SILENT:
endif

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

init:
	python3.11 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt;
	. venv/bin/activate; cd src/fastapi_app; poetry install
	. venv/bin/activate; cd src/streamlit_app; poetry install
	@echo "\n\033[0;32mYour dev environment is ready!\033[0m\n"

# Usual testing
test-backend:
	. venv/bin/activate; cd src/fastapi_app; \
	PYTHONPATH=. pytest tests -W ignore::DeprecationWarning $(coverage_params) $(ARGS)

test-frontend:
	. venv/bin/activate; cd src/streamlit_app; \
	PYTHONPATH=. pytest tests -W ignore::DeprecationWarning $(ARGS)


# Covered testing
coverage-backend: coverage_report_output ?= coverage_report
coverage-backend: coverage_params = --cov=app --cov-report=term-missing:skip-covered --cov-report=html:$(ROOT_DIR)/$(coverage_report_output) --cov-branch
coverage-backend: test-backend

docker-run:
	docker compose up --build $(ARGS)

format:
	( \
		. venv/bin/activate; cd src;\
		isort streamlit_app; black streamlit_app;\
		black fastapi_app; isort fastapi_app;\
	)

# Linter
lint-check: 
	$(MAKE) -k -$(MAKEFLAGS) lint-pylint; \
	$(MAKE) -k -$(MAKEFLAGS) lint-flake8; \
	$(MAKE) -k -$(MAKEFLAGS) lint-refurb; \

lint-pylint:
	. venv/bin/activate; cd src; \
	pylint streamlit_app --fail-under=7 --rcfile=$(ROOT_DIR)/src/.pylintrc $(ARGS) && \
	pylint fastapi_app/app --fail-under=10 --rcfile=$(ROOT_DIR)/src/.pylintrc $(ARGS); \

lint-flake8:
	. venv/bin/activate; cd src; \
	flake8 streamlit_app && \
	flake8 fastapi_app; \

lint-refurb:
	. venv/bin/activate; cd src; \
	refurb --enable-all streamlit_app; \
	refurb --enable-all fastapi_app/app; \

# Security
# It's necessary to run from root directory
security-backend:
	. venv/bin/activate; \
	bandit -r src/fastapi_app/app $(ARGS); \


security-frontend:
	. venv/bin/activate; \
	bandit -r src/streamlit_app/app $(ARGS); \
