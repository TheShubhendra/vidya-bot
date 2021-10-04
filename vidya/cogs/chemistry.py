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
import asyncio
from typing import TYPE_CHECKING, Optional, Union

from discord.ext.commands import (
    Cog,
    Context,
    command,
    )
from discord_components import Button
from mendeleev import element as get_element
from sqlalchemy.exc import NoResultFound

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
        """Fetch details about an Element."""
        if element is None:
            await ctx.send(
                "Please send element name (`case sensitive`)\
or atomic number with the command"
            )
            return

        def build_components(n):
            try:
                prev_el = get_element(n - 1)
                prev_button = Button(
                    label=f"{prev_el.name} ({prev_el.atomic_number})",
                    custom_id=str(prev_el.atomic_number),
                    style=1,
                )
            except NoResultFound:
                prev_button = Button(
                    label="No element",
                    style=1,
                    disabled=True,
                )
            try:
                next_el = get_element(n + 1)
                next_button = Button(
                    label=f"{next_el.name} ({next_el.atomic_number})",
                    custom_id=str(next_el.atomic_number),
                    style=1,
                )
            except NoResultFound:
                next_button = Button(
                    label="No element",
                    style=1,
                    disabled=True,
                )
            return [[prev_button, next_button]]

        try:
            el = get_element(element)
            message = await ctx.send(
                embed=await self.embed.element(el),
                components=build_components(el.atomic_number),
            )
            while True:
                try:
                    inter = await self.bot.wait_for(
                        "button_click",
                        timeout=500,
                        check=lambda i: i.channel == i.message.channel,
                    )
                    if inter.user != ctx.author:
                        await inter.respond(
                            content="These buttons are not for you."
                        )
                        continue
                    el = get_element(int(inter.component.custom_id))
                    await message.edit(
                        embed=await self.embed.element(el),
                        components=build_components(el.atomic_number),
                    )

                except asyncio.TimeoutError:
                    await message.disable_components()

        except NoResultFound:
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
