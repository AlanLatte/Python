include .env
export

# enumeration of * .py files storage or folders is required.
files_to_fmt 	?= app tests
files_to_check 	?= app tests

# Sphinx settings
SPHINX_BUILD 	?= sphinx-build
SPHINX_TEMPLATES ?= ./docs/_templates
SOURCE_DIR     	= ./docs
BUILD_DIR      	= ./docs/_build


## Default target
.DEFAULT_GOAL := run

## Build api docker containers
docker_up:
	docker-compose up --build -d

run:
	uvicorn app:create_app --host localhost --reload --port ${API_SERVER_PORT}

# Build sphinx docs
docs: build_docs rst_builder
build_docs:
	: # Build *.rst from docstrings
	poetry run sphinx-apidoc -f -o "$(SOURCE_DIR)" . -t="$(SPHINX_TEMPLATES)"


rst_builder:
	: # Build html pages from *.rst
	poetry run $(SPHINX_BUILD) -b html "$(SOURCE_DIR)" "$(BUILD_DIR)"



## Format all
fmt: format
format: remove_imports isort black docformatter add-trailing-comma


## Check code quality
chk: check
lint: check
check: flake8 black_check docformatter_check safety bandit

## Migrate database
migrate:
	poetry run python -m scripts.migrate

## Rollback migrations in database
migrate-rollback:
	poetry run python -m scripts.migrate --rollback

migrate-reload:
	poetry run python -m scripts.migrate --reload

## Remove unused imports
remove_imports:
	autoflake -ir --remove-unused-variables \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		${files_to_fmt}


## Sort imports
isort:
	isort ${files_to_fmt}


## Format code
black:
	black ${files_to_fmt}


## Check code formatting
black_check:
	black --check ${files_to_check}


## Format docstring PEP 257
docformatter:
	docformatter -ir ${files_to_fmt}


## Check docstring formatting
docformatter_check:
	docformatter -cr ${files_to_check}


## Check pep8
flake8:
	flake8 ${files_to_check}


## Check typing
mypy:
	mypy ${files_to_check}


## Check if all dependencies are secure and do not have any known vulnerabilities
safety:
	safety check --bare --full-report


## Check code security
bandit:
	bandit -r ${files_to_check} -x tests

## Add trailing comma works only on unix.
# an error is expected on windows.
add-trailing-comma:
	find ${files_to_fmt} -name "*.py" -exec add-trailing-comma '{}' \;
