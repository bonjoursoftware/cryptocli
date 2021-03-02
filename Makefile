DOCKER_RUN = docker run  --interactive --rm bonjoursoftware/cryptocli:local

.PHONY: all
all: fmt-check test static-check

.PHONY: docker-build
docker-build:
	@docker build -t bonjoursoftware/cryptocli:local . > /dev/null

.PHONY: test
test: docker-build
	@$(DOCKER_RUN) pytest \
		-v \
		-p no:cacheprovider \
		--no-header \
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

.PHONY: fmt-check
fmt-check:
	@$(DOCKER_RUN) black --line-length 120 --check .

.PHONY: fmt
fmt:
	@pipenv run black --line-length 120 .
