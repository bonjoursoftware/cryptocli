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


class TestCryptocurrency(TestCase):
    @httpretty.activate
    def test_last_trade_price_known_symbol(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/tickers/BTC-USD",
            body='{"symbol": "BTC-USD", "price_24h": 57400.6, "volume_24h": 1010.255527, "last_trade_price": 54864.4}',
            content_type="text/json",
        )
        assert 54864.4 == Cryptocurrency("BTC-USD").last_trade_price()

    @httpretty.activate
    def test_last_trade_price_unknown_symbol(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://api.blockchain.com/v3/exchange/tickers/BTC-XXX",
            body='{"error": "Internal Server Error"}',
            content_type="text/json",
            status=500,
        )
        with raises(CryptoCLIException):
            Cryptocurrency("BTC-XXX").last_trade_price()
