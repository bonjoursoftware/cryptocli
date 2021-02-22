DOCKER_RUN = docker run  --interactive --rm bonjoursoftware/cryptocli:local

.PHONY: docker-build
docker-build:
	@docker build -t bonjoursoftware/cryptocli:local . > /dev/null

.PHONY: test
test: docker-build
	@$(DOCKER_RUN) pytest -v --no-header -p no:cacheprovider

.PHONY: fmt
fmt:
	@pipenv run black --line-length 120 .
