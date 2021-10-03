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
# along with this program.  If not, see <https://www.gnu.org/licenses/>

from typing import TYPE_CHECKING, Optional, Union

import sqlalchemy
from discord.ext.commands import (
    Cog,
    Context,
    command,
)
from mendeleev import element as get_element

if TYPE_CHECKING:
    from vidya.bot import Vidya


class Chemistry(Cog):
    def __init__(self, bot: "Vidya"):
        self.bot = bot
        self.embed = self.bot.embed

    @command(aliases=["elem"])
    async def element(
        self,
        ctx: Context,
        element: Optional[Union[int, str]],
    ):
        if element is None:
            await ctx.send(
                "Please send element name (`case sensitive`)\
or atomic number with the command"
            )
            return
        try:
            el = get_element(element)
            await ctx.send(
                embed=self.embed.element(el),
            )
        except sqlalchemy.exc.NoResultFound:
            if isinstance(element, int):
                await ctx.send(
                    f"No chemical element found\
 with the atom number **{element}**."
                )
            else:
                await ctx.send(
                    f"No chemical element found\
 with the symbol **{element}. Please not that the symbol are case-sensitive."
                )


def setup(bot):
    bot.add_cog(Chemistry(bot))
