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
from functools import lru_cache
from typing import TYPE_CHECKING, Optional, Union
import discord
from discord.ext.commands import (
    Cog,
    Context,
    command,
    )
from mendeleev import element, Element
from sqlalchemy.exc import NoResultFound

if TYPE_CHECKING:
    from vidya.bot import Vidya

@lru_cache()
def get_element(e):
    return element(e)


class ElementButton(discord.ui.Button):
    async def callback(self, interaction: discord.Integration):
        await self.view.handle_callback(self, interaction)


class ElementView(discord.ui.View):
    def __init__(self, element: Element, cog: Cog) -> None:
        super().__init__(timeout=None)
        self.element = element
        self.cog = cog
        self.add_item(self.previos_button)
        self.add_item(self.next_button)

    @property
    def previous(self):
        try:
            return get_element(self.element.atomic_number - 1)
        except NoResultFound:
            return None

    @property
    def next(self):
        try:
            return get_element(self.element.atomic_number + 1)
        except NoResultFound:
            return None

    @property
    def next_button(self):
        el = self.next
        if el is None:
            return ElementButton(
                label="No element",
                disabled=True,
            )
        return ElementButton(
            label=f"{el.atomic_number} {el.name}",
            custom_id="next",
        )

    @property
    def previos_button(self):
        el = self.previous
        if el is None:
            return ElementButton(
                label="No element",
                disabled=True,
            )
        return ElementButton(
            label=f"{el.atomic_number} {el.name}",
            custom_id="previous",
        )



    async def handle_callback(self, button: ElementButton, interaction: discord.Interaction):
  
        if button.custom_id == "previous":
            self.element = self.previous
        elif button.custom_id == "next":
            self.element = self.next

        self.clear_items()
        self.add_item(self.previos_button)
        self.add_item(self.next_button)

        await interaction.response.edit_message(
            embed = await self.cog.embed.element(self.element),
            view=self,
        )

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

        try:
            el = get_element(element)
            view = ElementView(el, self)
            embed = await self.embed.element(el)
            await ctx.send(
                embed=embed,
                view=view,
            )
 
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
