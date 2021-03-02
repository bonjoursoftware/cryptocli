DOCKER_RUN = docker run  --interactive --rm bonjoursoftware/cryptocli:local

.PHONY: all
all: fmt test static-check

.PHONY: docker-build
docker-build:
	@docker build -t bonjoursoftware/cryptocli:local . > /dev/null

.PHONY: test
test: docker-build
	@$(DOCKER_RUN) pytest -v \
		--no-header \
		-p no:cacheprovider \
		--cov=cryptocli \
		--cov-fail-under=100 \
		--no-cov-on-fail

.PHONY: flake8
flake8: docker-build
	@$(DOCKER_RUN) flake8 --max-line-length 120

.PHONY: mypy
mypy: docker-build
	@$(DOCKER_RUN) mypy --strict ./**/*.py

.PHONY: static-check
static-check: flake8 mypy

.PHONY: fmt
fmt:
	@pipenv run black --line-length 120 .
