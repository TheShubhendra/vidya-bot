import asyncio
from typing import TYPE_CHECKING, Any, Optional
import discord

from discord.ext.commands import (
    Cog,
    Context,
    command,
    )

if TYPE_CHECKING:
    from vidya.bot import Vidya


class WordButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        return await self.view.handle_callback(self, interaction)


class WordView(discord.ui.View):
    def __init__(self, word, cog):
        self.word = word
        self.cog = cog
        super().__init__(timeout=None)
        for i, meaning in enumerate(word.meanings):
            self.add_item(
                WordButton(
                    label=meaning.get("partOfSpeech"),
                    custom_id=str(i),
                    disabled=True if i == 0 else False,
                    style=1,
                )
            )
    
    async def handle_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = self.cog.bot.embed.word(
            self.word,
            index=int(button.custom_id),
        )
        self.clear_items()
        for i, meaning in enumerate(self.word.meanings):
            self.add_item(
                WordButton(
                    label=meaning.get("partOfSpeech"),
                    custom_id=str(i),
                    disabled=True if i == int(button.custom_id) else False,
                    style=1,
                )
            )
        await interaction.response.edit_message(
            embed=embed,
            view=self,
        )




class English(Cog):
    def __init__(self, bot: "Vidya"):
        """English utility command cog."""
        self.bot = bot
        self.db = self.bot.db
        self.embed = self.bot.embed

    @command()
    async def word(self, ctx: Context, word: Optional[str]):
        """Get detailed information about a English word."""
        try:
            word = await self.bot.wapi.fetch_word(word)
        except ValueError:
            await ctx.send(
                f"🙄Who told you about this word *{word}*.\
It does't even exist in my dictionary."
            )
            return
        if len(word.meanings) < 2:
            embed = self.embed.word(word)
            await ctx.send(
                embed=embed,
            )
        else:
            view = WordView(word, self)
            embed = self.embed.word(word)
            message = await ctx.send(
                embed=embed,
                view=view,
            )

def setup(bot: "Vidya"):
    bot.add_cog(English(bot))
