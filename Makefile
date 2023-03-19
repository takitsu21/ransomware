install:
	poetry install
lint:
	autopep8 --in-place --aggressive --recursive -v .