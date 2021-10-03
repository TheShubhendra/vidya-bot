# distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from discord.ext.commands import (
    Cog,
    Context,
    command,
)


class Currency(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.redis = self.bot.redis
        self.embed = self.bot.embed

    @command()
    async def daily(self, ctx: Context):
        """Earn Daily Reward."""
        ttl = await self.redis.ttl(
            f"daily:{ctx.author.id}",
        )
        if ttl == -2:
            await self.redis.hincrby(
                f"user:{ctx.author.id}",
                "mudra",
                10000,
            )
            await self.redis.set(
                f"daily:{ctx.author.id}",
                "True",
                ex=24 * 3600,
            )
            embed = self.embed.default(
                title="Here is your daily reward",
                description="10,000 mudra has been deposited to your account.\nShow regular presence and get more rewards",
            )
            embed.add_field(
                name="Claim your next reward after 24 hour.",
                value="\u0004",
            )
            await ctx.send(embed=embed)
        else:
            time_left = ""
            hour = ttl // 3600
            if hour > 0:
                time_left += f" {hour} hour"
                ttl = ttl % 3600
            minute = ttl // 60
            if minute > 0:
                time_left += f" {minute} hour"
                ttl = ttl % 60
            if ttl > 0:
                time_left += f" and {ttl} second."
            embed = self.embed.default(
                title="Daily reward",
                description=f"You have already got your daily reward. Now claim your next reward after{time_left}",
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Currency(bot))
