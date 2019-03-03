YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @sh -c '\
    printf $(YELLOW); \
    echo "=> $$1"; \
    printf $(NC)' VALUE

GOALS = $(filter-out $@,$(MAKECMDGOALS))
PEP8_CLEANED = drf_action_permissions

.SILENT:  # Ignore output of make `echo` command


.PHONY: help  # Generate list of targets with descriptions
help:
	@$(INFO) "Commands:"
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 > \2/' | column -tx -s ">"


.PHONY: lint  # Run linting and code auto formatting
lint:
	@$(INFO) "Formatting..."
	@black $(PEP8_CLEANED)
	@$(INFO) "Sorting..."
	@isort -rc $(PEP8_CLEANED)
	@$(INFO) "Linting..."
	@autoflake --in-place --recursive $(PEP8_CLEANED)
	@$(INFO) "Checking complexity..."
	@xenon --max-absolute B --max-modules A --max-average A $(PEP8_CLEANED)


.PHONY: clean # Clean temp files from projects: .pyc. .pyo, __pycache__
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache .mypy_cache .coverage.*
	@$(INFO) "Python caching files has been cleaned"


.PHONY: test  # Test package
test:
	@pytest


.PHONY: watch  # Test package in watch mode
watch:
	@ptw


.PHONY: publish  # Bump version and publish to pypi
publish:
	@poetry version $(GOALS)
	@poetry publish --build
