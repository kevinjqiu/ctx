.PHONY: help clean clean-pyc clean-build list test test-all coverage docs release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 ctx test --max-line-length=120

test:
	CTX_CFG=test py.test

test-all:
	tox

coverage:
	coverage run --source ctx setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/ctx.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ ctx
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean
	python setup.py sdist
	python setup.py bdist_wheel upload
	ls -l dist

build-server-image:
	docker build -t ctx-server .

run-dev-container: build-server-image
	docker run --rm -it -v $(shell pwd):/app -p 8080:8080 ctx-server /bin/bash

sync-views:
	CTX_CFG=localhost python -c "from ctx import database; database.init(); from ctx import view; view.sync_views(database.db)"
