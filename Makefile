#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = santas_workshop_tour
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	@rm -rf .venv
	$(PYTHON_INTERPRETER)$(PYTHON_VERSION) -m venv .venv
	@echo ">>> New python interpreter environment created. Activate it using 'source .venv/bin/activate'"


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	


## Overwrite requirements.txt with your installed dependencies
.PHONY: freeze
freeze:
	$(PYTHON_INTERPRETER) -m pip freeze > requirements.txt


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 santas_workshop_tour
	isort --check --diff --profile black santas_workshop_tour
	black --check --config pyproject.toml santas_workshop_tour


## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml santas_workshop_tour


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Run tests
.PHONY: tests
tests:
	$(PYTHON_INTERPRETER) -m pytest santas_workshop_tour/tests/ -v


## Run santas_workshop_tour program
.PHONY: santas
santas:
	$(PYTHON_INTERPRETER) santas_workshop_tour/main.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
