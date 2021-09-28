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
import asyncio
import sys

import discord
import pip
from discord import Colour, Embed

from vidya.api import OpenTDBQuiz
from vidya.shop.item import Purchasable


class EmbedBuilder:
    def __init__(self, bot):
        self.bot = bot

    def default(self, *args, **kwargs):
        embed = Embed(*args, **kwargs)
        return embed

    def opentdb(self, quiz: OpenTDBQuiz):
        embed = self.default(
            title="Quiz",
            description=f"""**{quiz.question}**
**Catgory:** {quiz.category}
**Difficulty:** {quiz.difficulty}""",
        )
        return embed

    def opentdb_res(
        self,
        quiz: OpenTDBQuiz,
        user_answer: bool,
        time_took: float,
        score: float,
    ):
        if not user_answer:
            embed = self.default(
                title="Quiz",
                description=f"""**{quiz.question}**
**Catgory:** {quiz.category}
**Difficulty:** {quiz.difficulty}""",
                colour=Colour.red(),
            )
        else:
            embed = self.default(
                title="Quiz",
                description=f"""**{quiz.question}**
**Catgory:** {quiz.category}
**Difficulty:** {quiz.difficulty}""",
                colour=Colour.green(),
            )
            embed.add_field(
                name="Result",
                value=f"""**Time took:** {round(time_took,2)} second
**Score gain:** {score}""",
            )
            return embed

    def shop_item(self, item: Purchasable) -> Embed:
        embed = self.default(
            title=item.name,
            description=item.description,
        )
        embed.add_field(
            name="\u0004",
            value=f"**Buy:** {item.price}",
        )
        return embed

    def status(self) -> Embed:
        all_tasks = asyncio.tasks.all_tasks()
        embed = self.default(
            name="Bot Status",
            colour=Colour.blue(),
        )
        bot = self.bot
        embed.add_field(
            name="\u0004",
            value=f"""**Server Connected:** {len(bot.guilds)}
**User Connected:** {len(bot.users)}
**Total Commands:** {len(bot.commands)}""",
        )

        embed.add_field(
            name="\u0004",
            value=f"""**Active Tasks:** {len(all_tasks)}
**Uptime:** {bot.up_time} second
**Latency:** {bot.latency*10000} ms""",
        )
        version = sys.version_info
        embed.add_field(
            name="\u0004",
            value=f"""**Python:** {version.major}.{version.minor}.{version.micro}
**discord.py:** {discord.__version__}\n**pip:** {pip.__version__}""",
        )
        return embed
