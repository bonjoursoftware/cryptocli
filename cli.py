# CryptoCLI - A Python CLI that fetches live cryptocurrency prices
#
# https://github.com/bonjoursoftware/cryptocli
#
# Copyright (C) 2021 Bonjour Software Limited
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
from argparse import ArgumentParser
from threading import Event
from typing import Any, Tuple

from cryptocli.cryptocurrency import Cryptocurrency
from cryptocli.exceptions import CryptoCLIException


def parse_args() -> Tuple[Any, Any]:
    parser = ArgumentParser(description="fetches live cryptocurrency prices")
    parser.add_argument("-s", "--symbol", type=str, help="cryptocurrency symbol", default="BTC-GBP")
    parser.add_argument("-t", "--ticker", type=int, help="ticker interval in seconds", default=300)
    args = parser.parse_args()
    return args.symbol, args.ticker


def print_last_trade_price(symbol: str) -> None:
    try:
        print(Cryptocurrency().last_trade_price(symbol))
    except CryptoCLIException as ex:
        print(ex)


def main() -> None:
    symbol, ticker = parse_args()
    print_last_trade_price(symbol)
    crypto_ticker = Event()
    while not crypto_ticker.wait(ticker):
        print_last_trade_price(symbol)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
