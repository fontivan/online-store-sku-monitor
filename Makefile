# Makefile derived from https://web.archive.org/web/20240205205603/https://venthur.de/2021-03-31-python-makefiles.html

# Get the directory this Makefile is sitting in
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(ROOT_DIR)/$(VENV)/bin

all: pylint yamllint

$(VENV)-ci: src/requirements/ci.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r src/requirements/ci.txt
	touch $(VENV)

$(VENV)-usage: src/requirements/usage.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r src/requirements/usage.txt
	touch $(VENV)

.PHONY: run
run: $(VENV)-usage
	(cd src && $(BIN)/python online_store_sku_monitor.py)

.PHONY: pylint
pylint: $(VENV)-ci
	$(BIN)/pylint $(ROOT_DIR)/src/

.PHONY: yamllint
yamllint: $(VENV)-ci
	$(BIN)/yamllint .

clean:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
