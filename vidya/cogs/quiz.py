from typing import TYPE_CHECKING

from discord.ext.commands import (
    Cog,
    Context,
    command,
)

from vidya.ext import QuizHandler

if TYPE_CHECKING:
    from vidya.bot import Vidya


class Quiz(Cog):
    def __init__(self, bot: "Vidya"):
        """Cog for quiz."""
        self.bot = bot
        self.embed = bot.embed
        self.quiz = QuizHandler(bot)

    @command()
    async def quiz(self, ctx: Context):
        quizzes = await self.quiz.fetch()
        for quiz in quizzes:
            await self.quiz.send(ctx, quiz)


def setup(bot: "Vidya"):
    bot.add_cog(Quiz(bot))
