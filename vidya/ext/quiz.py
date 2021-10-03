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
import time
from typing import TYPE_CHECKING

from discord.ext.commands import Context
from discord_components import Button

from vidya.api import OpenTDB, OpenTDBQuiz

if TYPE_CHECKING:
    from vidya.bot import Vidya


class QuizHandler:
    def __init__(self, bot: "Vidya"):
        """Quiz handler."""
        self.bot = bot
        self.embed = self.bot.embed
        self.db = self.bot.db
        self.opentdb = OpenTDB()
        self.categories = {
            9: "General Knowledge",
            10: "Books",
            11: "Film",
            12: "Music",
            13: "Musicals & Theatres",
            14: "Television",
            15: "Video Games",
            16: "Board Games",
            17: "Science & Nature",
            18: "Computers",
            19: "Mathematics",
            20: "Mythology",
            21: "Sports",
            22: "Geography",
            23: "History",
            24: "Politics",
            25: "Art",
            26: "Celebrities",
            27: "Animals",
            28: "Vehicles",
            29: "Comics",
            30: "Science: Gadgets",
            31: "Japanese Anime & Manga",
            32: "Cartoon & Animations",
        }

    async def fetch(self, *args, **kwargs):
        quizzes = await self.opentdb.fetch(*args, **kwargs)
        return quizzes

    async def _send(
        self,
        ctx: Context,
        quiz: OpenTDBQuiz,
        timeout: int = 10,
    ):
        embed = self.embed.opentdb(quiz)

        def button(o):
            return Button(label=o, custom_id=o)

        components = list(map(button, quiz.options))
        message = await ctx.send(
            embed=embed,
            components=[components],
        )
        start = time.time()
        try:
            while True:
                interaction = await self.bot.wait_for(
                    "button_click",
                    timeout=timeout,
                    check=lambda i: i.channel == i.message.channel,
                )
                if interaction.user != ctx.author:
                    await interaction.respond(
                        content="""This quiz is not supposed for you.\n
Please bother yourself to send `vid quiz`."""
                    )
                    continue
                break
            end = time.time()
            res_components = []
            user_answer = True
            for i in components:
                if quiz.check(i.custom_id):
                    style = 3
                elif i.custom_id == interaction.custom_id:
                    style = 4
                    user_answer = False
                else:
                    style = 2
                button = Button(
                    label=i.label,
                    style=style,
                    disabled=True,
                )
                res_components.append(button)
            score = await self.update_score(
                ctx.student,
                user_answer,
                time_took=end - start,
            )
            await interaction.message.edit(
                embed=self.embed.opentdb_res(
                    quiz,
                    user_answer,
                    end - start,
                    score,
                ),
                components=[res_components],
            )
        except asyncio.TimeoutError:
            await message.disable_components()

    async def send(self, ctx: Context, quiz):
        await self._send(ctx, quiz)

    async def update_score(self, student, user_answer: bool, time_took):
        if user_answer:
            score_change = 5 + (20 / int(time_took))
            await self.db.update_score(student, score_change)
        else:
            score_change = 0
        return score_change
