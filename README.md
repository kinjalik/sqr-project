# SQR Project

### Dev setup
1. `make init`
   also activate venv in your work shell via `source venv/bin/activate`
2. `make format` for code format
3. `make lint-check` for check code quality

### Run&Build Docker container
`make docker-run`

### Run checks
- Backend tests: `make test-backend`
- Backend security: `make security-backend`
- Coverage: `make coverage-backend`
- Linter: `make lint-check`
- Frontend security: `make security-frontend`