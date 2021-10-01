#!/usr/bin/python
# -*- coding: utf-8 -*-
# vidya - A Discord bot to play quizzes and learn with fun.
# Copyright (C) 2021 Shubhendra Kushwaha
# Email: shubhendrakushwaha94@gmail.com
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import TYPE_CHECKING

from discord import Embed

from .item import Purchasable

if TYPE_CHECKING:
    from vidya.bot import Vidya


class Shop:
    def __init__(self, bot: "Vidya") -> None:
        """Bot Shop."""
        self.bot = bot
        self.embed = self.bot.embed
        self.items = []

    def add(self, item: Purchasable) -> None:
        self.items.append(item)

    def search(self, item_id: str) -> Purchasable:
        results = [item for item in self.items if item.id == item_id]
        if len(results) == 0:
            results = [item for item in self.items if item.name == item_id]
        return results[0]

    def show_item(self, item_id: str) -> Embed:
        item = self.search(item_id)
        return self.embed.shop_item(item)

    def __len__(self) -> int:
        """Returns item count in the shop."""
        return len(self.items)
