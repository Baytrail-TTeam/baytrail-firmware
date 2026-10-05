PYTHON ?= python3
.PHONY: validate list index
validate:
	$(PYTHON) scripts/catalog.py validate
list:
	$(PYTHON) scripts/catalog.py list
index:
	$(PYTHON) scripts/catalog.py index
