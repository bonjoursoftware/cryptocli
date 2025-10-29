#!/usr/bin/env python
# CryptoCLI - A Python CLI that fetches live cryptocurrency prices
#
# https://github.com/bonjoursoftware/cryptocli
#
# Copyright (C) 2021 - 2025 Bonjour Software Limited
#
# https://bonjoursoftware.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see
# https://github.com/bonjoursoftware/cryptocli/blob/master/LICENSE
from argparse import ArgumentParser, Namespace
from threading import Event

from cryptocli.cryptocurrency import Cryptocurrency
from cryptocli.exceptions import CryptoCLIException


def parse_args() -> None:
    parser = ArgumentParser(
        description="Cryptocurrency command-line tool",
        epilog="https://github.com/bonjoursoftware/cryptocli",
        prog="docker run bonjoursoftware/cryptocli",
    )
    parser.set_defaults(func=lambda _: print(parser.format_help()))

    subparsers = parser.add_subparsers()

    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("-s", "--symbol", type=str, required=True, help="cryptocurrency symbol")
    find_parser.set_defaults(func=find_symbols)

    price_parser = subparsers.add_parser("price")
    price_parser.add_argument("-s", "--symbol", type=str, help="cryptocurrency symbol", default="BTC-GBP")
    price_parser.add_argument("-t", "--ticker", type=int, help="ticker interval in seconds")
    price_parser.set_defaults(func=watch_last_trade_price)

    args = parser.parse_args()
    args.func(args)


def watch_last_trade_price(args: Namespace):
    last_trade_price(args.symbol)
    if args.ticker:
        crypto_ticker = Event()
        while not crypto_ticker.wait(args.ticker):
            last_trade_price(args.symbol)


def last_trade_price(symbol: str) -> None:
    try:
        print(Cryptocurrency().last_trade_price(symbol))
    except CryptoCLIException as ex:
        print(ex)


def find_symbols(args: Namespace) -> None:
    try:
        print(Cryptocurrency().find_symbols(args.symbol))
    except CryptoCLIException as ex:
        print(ex)


def main() -> None:
    parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
