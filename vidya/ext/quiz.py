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
from random import shuffle
from typing import TYPE_CHECKING
import discord

from discord.ext.commands import Context
from pandas import options

from vidya.api import OpenTDB, OpenTDBQuiz

if TYPE_CHECKING:
    from vidya.bot import Vidya


class QuizButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        await self.view.handle_callback(self, interaction)


class QuizView(discord.ui.View):
    def __init__(self, quiz, handler, student, timeout: float):
        self.student = student
        self.start = time.time()
        self.quiz = quiz
        self.handler = handler
        super().__init__(timeout=timeout)
        def button(o):
            return QuizButton(label=o, custom_id=o)

        buttons = list(map(button, quiz.options))
        shuffle(buttons)
        for i in buttons:
            self.add_item(i)
 


    async def handle_callback(self, button: QuizButton, interaction: discord.Interaction):
            end = time.time()
            self.clear_items()
            user_answer = True
            for i in self.children:
                if self.uiz.check(button.custom_id):
                    style = 3
                elif i.custom_id == interaction.custom_id:
                    style = 4
                    user_answer = False
                else:
                    style = 2
                button = QuizButton(
                    label=i.label,
                    style=style,
                    disabled=True,
                )
                self.add_item(button)
            score = await self.handler.update_score(
                self.student,
                user_answer,
                time_took=end - self.start,
            )
            await interaction.message.edit(
                embed=self.handler.embed.opentdb_res(
                    self.quiz,
                    user_answer,
                    end - self.start,
                    score,
                ),
                view=self,
            )
 

    

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
        message = await ctx.send(
            embed=embed,
            view=QuizView(quiz, self, ctx.student, timeout),
        )

    async def send(self, ctx: Context, quiz):
        await self._send(ctx, quiz)

    async def update_score(self, student, user_answer: bool, time_took):
        if user_answer:
            score_change = 5 + (20 / int(time_took))
            await self.db.update_score(student, score_change)
        else:
            score_change = 0
        return score_change
