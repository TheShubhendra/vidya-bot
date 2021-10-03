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
from typing import Dict, List
from discord.ext.commands import (
    Command,
    Cog,
    HelpCommand,
    )

Mapping = Dict[Cog, List[Command]]


class VidyaHelpCommand(HelpCommand):
    """Custom help command."""
    def __init__(self):
        super().__init__()

    async def send_bot_help(
        self,
        mapping: Mapping,
    ):
        """Method to send help for all commands."""
        embed = self.context.bot.embed.bot_help(mapping)
        await self.context.send(embed=embed)

    async def send_command_help(self, command: Command):
        """Method to send help for a specific command."""
        destination = self.get_destination()
        await destination.send(embed=self.context.bot.embed.command_help(command))
