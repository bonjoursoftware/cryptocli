# CryptoCLI - A Python CLI that fetches live cryptocurrency prices
#
# https://github.com/bonjoursoftware/cryptocli
#
# Copyright (C) 2021 - 2026 Bonjour Software Limited
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
from unittest import TestCase

import httpretty
from pytest import raises

from cryptocli.cryptocurrency import Cryptocurrency
from cryptocli.exceptions import CryptoCLIException


class TestLastTradePrice(TestCase):
    @httpretty.activate
    def test_known_symbol(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://duckduckgo.com/js/spice/currency_convert/1/BTC/GBP",
            body='{"from":"BTC","amount":1.0,"to":[{"quotecurrency":"GBP","mid":52895.8485534152}]}',
        )
        assert {"symbol": "BTC-GBP", "price": 52895.8485534152} == Cryptocurrency().price("BTC-GBP")

    @httpretty.activate
    def test_unknown_symbol(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://duckduckgo.com/js/spice/currency_convert/1/BTC/XXX",
            body='{"from":"BTC","amount":1.0,"to":[]}',
            status=200,
        )
        with raises(CryptoCLIException):
            Cryptocurrency().price("BTC-XXX")

    @httpretty.activate
    def test_request_exception(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://duckduckgo.com/js/spice/currency_convert/1/???/XXX",
            status=500,
        )
        with raises(CryptoCLIException):
            Cryptocurrency().price("???-XXX")
