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
import logging

from decouple import config
from discord.ext.commands import Bot

TOKEN = config("TOKEN")
LOGGING = int(config("LOGGING", 20))

logging.basicConfig(
    format="%(name)s - %(message)s",
    level=LOGGING,
)


vidya = Bot(
    command_prefix="vid",
    case_insensitive=True,
    strip_after_prefix=True,
)


vidya.run(TOKEN)
