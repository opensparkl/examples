# Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
# Author <miklos@sparkl.com> Miklos Duma

PYTHON_VERSION ?= 3
CFG_PATH ?= Mandatory

ifeq ($(PYTHON_VERSION), 2)
PYTHON := python
PEP := pep8
PIP := pip
else
PYTHON := python3
PEP := pycodestyle
PIP := pip3
endif

.PHONY: help
help:
	@echo "Try one of the following:"
	@echo "test|test_basic|test_auth|lint"


.PHONY: lint
lint: pep8
	@${PYTHON} -m ${PEP} python_scripts/*.py
	@${PYTHON} -m ${PEP} python_scripts/log_framework/*.py
	@${PYTHON} -m ${PEP} tests/*.py
	@${PYTHON} -m pylint python_scripts/*.py --disable=superfluous-parens --disable=relative-import
	@${PYTHON} -m pylint python_scripts/log_framework/*.py --disable=unused-argument --disable=import-error --disable=no-name-in-module --disable=broad-except --disable=superfluous-parens --disable=relative-import
	@${PYTHON} -m pylint tests/*.py --disable=redefined-outer-name --disable=superfluous-parens --disable=relative-import

.PHONY: test
test: test_basic test_auth


.PHONY: test_basic
test_basic: pytest $(CFG_PATH)
	@echo Running basic tests.
	@${PYTHON} -m pytest -s tests/no_auth/

.PHONY: test_auth
test_auth: pytest $(CFG_PATH)
	@echo Running tests that need extra settings.
	@${PYTHON} -m pytest -s tests/with_auth/

$(CFG_PATH):
	$(error Must have valid CFG_PATH: $@)

.PHONY: pep8
pep8:
	@$(PIP) list --format=columns | grep $(PEP)


.PHONY: pytest
pytest:
	@$(PIP) list --format=columns | grep pytest

