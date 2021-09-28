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
import discord
from discord.ext import commands

BOT_INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=892272428728844309&permissions=309237763136&scope=bot"  # noqa

SERVER_INVITE_LINK = "https://discord.gg/SEnqh73qYj"


class BotSpecific(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = self.bot.embed

    @commands.command()
    async def ping(self, ctx):
        """Check bot latency."""
        embed = self.embed.default(colour=discord.Colour.dark_blue())
        embed.add_field(
            name="Pong!",
            value=(f"Latency: {round(self.bot.latency * 1000)}ms"),
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Invites bot to your server."""
        await ctx.send(BOT_INVITE_LINK)

    @commands.command()
    async def status(self, ctx):
        """Bot status."""
        await ctx.send(embed=self.embed.status())


def setup(bot):
    x = BotSpecific(bot)
    bot.add_cog(x)
