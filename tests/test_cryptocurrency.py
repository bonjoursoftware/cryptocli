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
            uri="https://duckduckgo.com/js/spice/cryptocurrency/BTC/USD/1",
            body='ddg_spice_cryptocurrency(\n{"data":{"amount":1,"id":1,"last_updated":"2025-10-29T16:02:00.000Z","name":"Bitcoin","quote":{"2781":{"last_updat'
            'ed":"2025-10-29T16:04:04.000Z","price":111434.752497096}},"symbol":"BTC"},"status":{"error_code":0,"timestamp":"2025-10-29T16:04:56.980Z"}});',
        )
        assert {"symbol": "BTC-USD", "price": 111434.752497096} == Cryptocurrency().price("BTC-USD")

    @httpretty.activate
    def test_unknown_symbol(self) -> None:
        httpretty.register_uri(
            method=httpretty.GET,
            uri="https://duckduckgo.com/js/spice/cryptocurrency/BTC/XXX/1",
            body='ddg_spice_cryptocurrency(\n{"error":"internal"});',
            status=400,
        )
        with raises(CryptoCLIException):
            Cryptocurrency().price("BTC-XXX")
