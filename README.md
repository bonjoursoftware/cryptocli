# CryptoCLI

[![CI](https://github.com/bonjoursoftware/cryptocli/actions/workflows/main.yml/badge.svg)](https://github.com/bonjoursoftware/cryptocli/actions/workflows/main.yml)
[![CodeQL](https://github.com/bonjoursoftware/cryptocli/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/bonjoursoftware/cryptocli/actions/workflows/codeql-analysis.yml)

[Bonjour Software](https://bonjour.software) CryptoCLI is a cryptocurrency command-line tool.

## Requirements

- Docker runtime

## Usage

- fetch last trade price for a given cryptocurrency symbol:

```shell
docker run bonjoursoftware/cryptocli price --symbol BTC-GBP
```

Tip: prices can be polled at regular intervals with the `--ticker` argument (in seconds):

```shell
docker run bonjoursoftware/cryptocli price --symbol BTC-GBP --ticker 300
```

- print manual:

```shell
docker run bonjoursoftware/cryptocli --help
```

Tip: the `--help` argument also works on subcommands:

```shell
docker run bonjoursoftware/cryptocli price --help
```
