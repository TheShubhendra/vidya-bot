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
import sys

import discord
import pip
from discord import Colour, Embed, User
from mendeleev import Element

from vidya.api import OpenTDBQuiz, Word
from vidya.shop.item import Purchasable


class EmbedBuilder:
    def __init__(self, bot):
        """Embed builder."""
        self.bot = bot
        self.db = self.bot.db

    def default(self, *args, **kwargs):
        embed = Embed(*args, **kwargs)
        return embed

    def opentdb(self, quiz: OpenTDBQuiz):
        embed = self.default(
            title="Quiz",
            description=f"""**{quiz.question}**
**Catgory:** {quiz.category}
**Difficulty:** {quiz.difficulty}""",
        )
        return embed

    def opentdb_res(
        self,
        quiz: OpenTDBQuiz,
        user_answer: bool,
        time_took: float,
        score: float,
    ):
        if not user_answer:
            embed = self.default(
                title="Quiz",
                description=f"""**{quiz.question}**
**Catgory:** {quiz.category}
**Difficulty:** {quiz.difficulty}""",
                colour=Colour.red(),
            )
        else:
            embed = self.default(
                title="Quiz",
                description=f"""**{quiz.question}**
**Catgory:** {quiz.category}
**Difficulty:** {quiz.difficulty}""",
                colour=Colour.green(),
            )
            embed.add_field(
                name="Result",
                value=f"""**Time took:** {round(time_took,2)} second
**Score gain:** {score}""",
            )
            return embed

    def shop_item(self, item: Purchasable) -> Embed:
        embed = self.default(
            title=item.name,
            description=item.description,
        )
        embed.add_field(
            name="\u0004",
            value=f"**Buy:** {item.price}",
        )
        return embed

    def status(self) -> Embed:
        all_tasks = asyncio.tasks.all_tasks()
        embed = self.default(
            name="Bot Status",
            colour=Colour.blue(),
        )
        bot = self.bot
        embed.add_field(
            name="\u0004",
            value=f"""**Server Connected:** {len(bot.guilds)}
**User Connected:** {len(bot.users)}
**Total Commands:** {len(bot.commands)}""",
        )

        embed.add_field(
            name="\u0004",
            value=f"""**Active Tasks:** {len(all_tasks)}
**Uptime:** {bot.up_time} second
**Latency:** {bot.latency*10000} ms""",
        )
        version = sys.version_info
        embed.add_field(
            name="\u0004",
            value=f"""**Python:** {version.major}.{version.minor}.{version.micro}
**discord.py:** {discord.__version__}\n**pip:** {pip.__version__}""",
        )
        return embed

    async def profile(self, user: User):
        student = await self.db.get_student(user.id)
        if student is None:
            return Embed(
                title="User not Found",
                description="First Introduce me to them",
            )
        commands_data = await self.db.get_commands_status(student.id)
        total_issued = sum([c.count for c in commands_data])
        avatar = user.avatar_url_as(format="png")
        embed = Embed(
            title=f"{user.display_name}'s profile",
            description=f"""**Score**: {student.score}
**Commands Issued:** {total_issued}""",
        )
        embed.set_thumbnail(url=avatar)
        return embed

    def word(self, word: Word, index: int = 0):
        meaning = word.meanings[index]
        embed = Embed(
            title=f"**{word.word} ({meaning.get('partOfSpeech')})**",
            description=f"**Origin:** *{word.origin}*"
            if word.origin
            else "\u0004",  # noqa
        )
        definitions = meaning.get("definitions")
        for defs in definitions:
            string = f"**Example:** *{defs.get('example')}*"
            synonyms = defs.get("synonyms")
            antonyms = defs.get("antonyms")
            if len(synonyms) > 0:
                string += f"\n**Synonyms:** *{', '.join(synonyms)}*"
            if len(antonyms) > 0:
                string += f"\n**Antonyms:** *{', '.join(antonyms)}"
            num_of_fields = len(string) // 1024 + 1
            for i in range(num_of_fields):
                embed.add_field(
                    name=f"**{defs.get('definition')}**"
                    if i == 0
                    else "\u0004",  # noqa
                    value=string[i * 1024 : (i + 1) * 1024],
                )
        return embed

    def element(self, el: Element):
        atomic_structure = [
            ("Atomic Radius", "atomic_radius", "pm"),
            ("Atomic Volume", "atomic_volume", "cm³/mol"),
            ("Atomic Weight", "atomic_weight", ""),
            ("Density at 295K", "density", "g/cm³"),
            ("Mass Number", "mass_number", ""),
            ("Period", "period", ""),
            ("Metallic Radius", "metallic_radius", "pm"),
            ("Ground state electron configuration", "econf", ""),
            ("Geochemical classification", "geochemical_class", ""),
            ("Goldchmidt classification", "goldschmidt_class", ""),
            ("Van der Waals radius", "vdw_radius", ""),
        ]
        specific_values = [
            ("Evaporation Heat", "evaporation_heat", "kJ/mol"),
            ("Fusion Heat", "fusion_heat", " KJ/mol"),
            ("Boiling Point", "boiling_point", "K"),
            ("Melting point", "melting_point", ""),
            ("Specific heat @ 20 C ", "specific_heat", "J/(g mol)"),
            ("Thermal conductivity @25 C", "thermal_conductivity", " W/(m K)"),
            ("Gas basicity", "gas_basicity", "KJ/mol"),
            ("Pettifor Scale", "pettifor_number", ""),
        ]
        misc = [
            ("Is Radioactive", "is_radioactive", ""),
            ("Is Monoisotopick", "is_monoisotopic", ""),
            ("Oxidation states", "oxistates", ""),
            ("Proton Affinity", "proton_affinity", ""),
            ("Annotation", "annotation", ""),
            ("Electron Affinity", "electron_affinity", "eV"),
            ("Dipole polarizability", "dipole_polarizability", ""),
            ("Dipole polarizability uncertainty", "dipole_polarizability_unc", ""),
            ("Abundant in the earth Crush", "abundance_crust", "mg/Kg"),
            ("Abundance in the seas", "abundance_sea", "mg/L"),
            ("Lattice Constant", "lattice_constant", ""),
            ("Lattice Structure", "lattice_structure", ""),
        ]

        def func(x):
            a, b, c = x
            if not getattr(el, b):
                return ""
            return f"{a}: **{getattr(el,b)}**{c}\n"

        group = (
            f"{el.group.group_id} {el.group.name} ({el.group.symbol})"
            if el.group
            else "N/A"
        )
        if el.cpk_color:
            r, g, b = tuple(
                int(el.cpk_color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)
            )
            colour = Colour.from_rgb(r, g, b)
        else:
            colour = Colour.default()
        embed = self.default(
            title=f"{el.name} - {el.symbol}({el.atomic_number})",
            description=el.description,
            colour=colour,
        )
        value = "".join(list(map(func, atomic_structure)))
        embed.add_field(
            name="Atomic Structure",
            value=value if len(value) > 0 else "Data not available",
        )
        value = "".join(list(map(func, specific_values)))
        value += f"Block: **{el.block}** Group: **{group}**"
        embed.add_field(
            name="Specific Values",
            value=value if len(value) > 0 else "Data not available",
        )
        value = "".join(list(map(func, misc)))
        if el.electrophilicity():
            value += f"Electro philicity {el.electrophilicity()}eV"

        embed.add_field(
            name="Miscellaneous",
            value=value if len(value) > 0 else "Data not available",
        )
        embed.add_field(
            name="\u0004",
            value=f"""
Name Origin:** {el.name_origin}**

Source: **{el.sources}**

Application: **{el.uses}**
""",
        )
        return embed
