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
from requests import get
from requests.exceptions import RequestException
from typing import Any, Callable, Dict

from cryptocli.exceptions import CryptoCLIException


class Cryptocurrency:
    def last_trade_price(self, symbol: str) -> Dict[str, Any]:
        return self._get(
            url=f"https://duckduckgo.com/js/spice/cryptocurrency/{symbol.split('-')[0]}/{symbol.split('-')[1]}/1",
            read_response=lambda response: {
                "symbol": symbol,
                "last_trade_price": float(next(iter(loads(response)["data"]["quote"].values()))["price"]),
            },
            error_msg=f"unable to fetch {symbol} last trade price",
        )

    @staticmethod
    def _get(url: str, read_response: Callable[[str], Dict[Any, Any]], error_msg: str) -> Dict[Any, Any]:
        try:
            response = get(url=url)
            response.raise_for_status()
            return read_response(response.text.replace("ddg_spice_cryptocurrency(\n", "").replace(");", ""))
        except RequestException as ex:
            raise CryptoCLIException(f"{error_msg}: {ex}") from None
