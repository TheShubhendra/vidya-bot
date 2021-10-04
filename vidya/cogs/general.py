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
from typing import Optional

from discord import User
from discord.ext.commands import (
    Cog,
    Context,
    command,
    )


class General(Cog):
    def __init__(self, bot):
        """General Cog."""
        self.bot = bot
        self.db = self.bot.db
        self.embed = self.bot.embed

    @command()
    async def profile(self, ctx: Context, user: Optional[User]):
        """Shows profile."""
        if user is None:
            user = ctx.author
        embed = await self.embed.profile(user)
        await ctx.send(
            embed=embed,
        )


def setup(bot):
    bot.add_cog(General(bot))
