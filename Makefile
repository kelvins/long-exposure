code-check:
	@flake8 src/ tests/
	@black --check --diff -v src/ tests/

runtests:
	@pytest -vv tests/