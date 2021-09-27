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
from discord_components import ComponentsBot

from .database import DatabaseManager
from .handler import EmbedBuilder, QuizHandler


class Vidya(ComponentsBot):
    _instance = None

    def __init__(self, *args, **kwargs):
        if Vidya._instance is not None:
            raise Exception("Vidya class has been already initialised.")
        super().__init__(*args, **kwargs)
        try:
            self.db = DatabaseManager(kwargs["database_url"])
        except KeyError:
            raise ValueError("Please pass required parameters.")
        self.embed = EmbedBuilder(self)
        self.quiz = QuizHandler(self)
        Vidya._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise Exception("Vidya class is not initialised yet.")
        return cls._instance

    async def on_ready(self):
        @self.before_invoke
        async def ensure_a_student(context):
            dc_id = context.author.id
            student = await self.db.get_student(dc_id)
            if student is None:
                student = await self.db.add_student(
                    dc_id,
                    context.author.name + "#" + context.author.discriminator,
                )
                student = await self.db.get_student(dc_id)
            context.student = student

        @self.after_invoke
        async def record_command(context):
            await self.db.record_command(
                context.student.id,
                context.command.name,
            )
