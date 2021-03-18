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
import httpretty

from pytest import raises
from unittest import TestCase

from cryptocli.cryptocurrency import Cryptocurrency
from cryptocli.exceptions import CryptoCLIException


class TestLastTradePrice(TestCase):
    @httpretty.activate
    def test_known_symbol(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/tickers/BTC-USD",
            body='{"symbol": "BTC-USD", "price_24h": 57400.6, "volume_24h": 1010.255527, "last_trade_price": 54864.4}',
            content_type="text/json",
        )
        assert {"symbol": "BTC-USD", "last_trade_price": 54864.4} == Cryptocurrency().last_trade_price("BTC-USD")

    @httpretty.activate
    def test_unknown_symbol(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/tickers/BTC-XXX",
            body='{"error": "Internal Server Error"}',
            content_type="text/json",
            status=500,
        )
        with raises(CryptoCLIException):
            Cryptocurrency().last_trade_price("BTC-XXX")


class TestSymbols(TestCase):
    @httpretty.activate
    def test_list(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/symbols",
            body='{"LTC-BTC": {"id":23}, "XLM-EUR": {"id": 11}, "BTC-GBP": {"id": 35}, "LTC-EUR": {"id": 21}}',
            content_type="text/json",
        )
        assert {1: "BTC-GBP", 2: "LTC-BTC", 3: "LTC-EUR", 4: "XLM-EUR"} == Cryptocurrency().symbols()

    @httpretty.activate
    def test_can_not_list(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/symbols",
            body='{"error": "Internal Server Error"}',
            content_type="text/json",
            status=500,
        )
        with raises(CryptoCLIException):
            Cryptocurrency().symbols()


class TestFindSymbols(TestCase):
    @httpretty.activate
    def test_symbols_found(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/symbols",
            body='{"LTC-BTC": {"id":23}, "XLM-EUR": {"id": 11}, "BTC-GBP": {"id": 35}, "LTC-EUR": {"id": 21}}',
            content_type="text/json",
        )
        assert ["BTC-GBP", "LTC-BTC"] == Cryptocurrency().find_symbols("btc")

    @httpretty.activate
    def test_no_match(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/symbols",
            body='{"LTC-BTC": {"id":23}, "XLM-EUR": {"id": 11}, "BTC-GBP": {"id": 35}, "LTC-EUR": {"id": 21}}',
            content_type="text/json",
        )
        assert [] == Cryptocurrency().find_symbols("banana")

    @httpretty.activate
    def test_can_not_find_symbols(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/symbols",
            body='{"error": "Internal Server Error"}',
            content_type="text/json",
            status=500,
        )
        with raises(CryptoCLIException):
            Cryptocurrency().find_symbols("whatever")
