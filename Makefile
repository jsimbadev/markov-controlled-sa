.DEFAULT_GOAL := render
.NOTPARALLEL:

QUARTO ?= quarto
PYTHON ?= python3
PORT ?= 4200
export XDG_CACHE_HOME ?= $(CURDIR)/.quarto/cache
export TEXMFVAR ?= _output/tex-var
export TEXMFCACHE ?= _output/tex-cache

.PHONY: preview html pdf render clean check check-source sync-macros

preview: sync-macros
	$(QUARTO) preview index.qmd --to html --port $(PORT)

html: sync-macros
	$(QUARTO) render index.qmd --to html

pdf: sync-macros
	$(QUARTO) render index.qmd --to pdf

render: sync-macros
	$(QUARTO) render --to all

sync-macros:
	$(PYTHON) scripts/sync-macros.py

check-source:
	$(PYTHON) scripts/sync-macros.py --check
	$(PYTHON) scripts/check-labels.py
	$(PYTHON) scripts/check-citations.py
	$(PYTHON) -m unittest discover -s tests -v

check: check-source
	$(PYTHON) scripts/check-render.py --quarto "$(QUARTO)"

clean:
	$(PYTHON) scripts/clean.py
