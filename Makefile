#!/usr/bin/env python3

install:
	poetry install

run:
	poetry run laby

shell:
	poetry shell

build:
	poetry build

publish:
	poetry publish --dry-run

package-install
	python3 -m pip install dist/*.whl
