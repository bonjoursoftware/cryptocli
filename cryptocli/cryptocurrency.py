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
from json import loads
from typing import Any, Callable, Dict

from requests import get
from requests.exceptions import RequestException

from cryptocli import _raise
from cryptocli.exceptions import CryptoCLIException


class Cryptocurrency:
    def price(self, symbol: str) -> Dict[str, Any]:
        return self._get(
            url=f"https://duckduckgo.com/js/spice/currency_convert/1/{symbol.split('-')[0]}/{symbol.split('-')[1]}",
            read_response=lambda response: {
                "symbol": symbol,
                "price": float(next(iter(loads(response)["to"]))["mid"]),
            },
            error_msg=f"unable to fetch {symbol} last trade price",
        )

    @staticmethod
    def _get(url: str, read_response: Callable[[str], Dict[Any, Any]], error_msg: str) -> Dict[Any, Any]:
        try:
            response = get(url=url)
            response.raise_for_status()
            return read_response(response.text) if response.json()["to"] else _raise(CryptoCLIException(f"{error_msg}: unknown symbol"))
        except RequestException as ex:
            raise CryptoCLIException(f"{error_msg}: {ex}") from None
