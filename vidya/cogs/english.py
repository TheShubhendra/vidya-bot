import asyncio
from typing import TYPE_CHECKING, Optional

from discord.ext.commands import (
    Cog,
    Context,
    command,
)
from discord_components import Button

if TYPE_CHECKING:
    from vidya.bot import Vidya


class English(Cog):
    def __init__(self, bot: "Vidya"):
        """English utility command cog."""
        self.bot = bot
        self.db = self.bot.db
        self.embed = self.bot.embed

    @command()
    async def word(self, ctx: Context, word: Optional[str]):
        """Get detailed information about a English word."""
        word = await self.bot.wapi.fetch_word(word)
        if len(word.meanings) < 2:
            embed = self.embed.word(word)
            await ctx.send(
                embed=embed,
            )
        else:
            components = [
                [
                    Button(
                        label=mean.get("partOfSpeech"),
                        custom_id=str(i),
                        disabled=True if i == 0 else False,
                        style=1,
                    )
                    for i, mean in enumerate(word.meanings)
                ]
            ]

            embed = self.embed.word(word)
            message = await ctx.send(
                embed=embed,
                components=components,
            )
            while True:
                try:
                    inter = await self.bot.wait_for(
                        "button_click",
                        check=lambda i: i.message == message,
                        timeout=20,
                    )
                    index = inter.component.custom_id
                    components = [
                        [
                            Button(
                                label=mean.get("partOfSpeech"),
                                custom_id=str(i),
                                disabled=True if i == int(index) else False,
                                style=1,
                            )
                            for i, mean in enumerate(word.meanings)
                        ]
                    ]
                    embed = self.embed.word(
                        word,
                        index=int(index),
                    )
                    await inter.message.edit(
                        embed=embed,
                        components=components,
                    )
                except asyncio.TimeoutError:
                    await message.disable_components()


def setup(bot: "Vidya"):
    bot.add_cog(English(bot))
