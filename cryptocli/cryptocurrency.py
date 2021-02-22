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
from dataclasses import dataclass
from requests import get
from requests.exceptions import RequestException

from cryptocli.exceptions import CryptoCLIException


@dataclass
class Cryptocurrency:
    symbol: str

    def last_trade_price(self) -> float:
        try:
            response = get(url=f"https://api.blockchain.com/v3/exchange/tickers/{self.symbol}")
            response.raise_for_status()
            return float(response.json()["last_trade_price"])
        except RequestException as ex:
            raise CryptoCLIException(f"unable to fetch {self.symbol} last trade price: {ex}") from None
