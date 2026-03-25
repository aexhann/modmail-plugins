import discord
from discord.ext import commands, tasks

from core import checks, utils
from core.models import PermissionLevel, getLogger

logger = getLogger(__name__)


class Branding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_lock.start()

    def cog_unload(self):
        self.status_lock.cancel()

    @tasks.loop(seconds=20)
    async def status_lock(self):
        desired_text = "Hosted by Kairo"

        current = self.bot.activity

        if not current or current.name != desired_text:
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=desired_text
                ),
                status=discord.Status.online
            )

    @status_lock.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=["info"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    @utils.trigger_typing
    async def about(self, ctx):
        """Shows information about this bot."""

        embed = discord.Embed(
            color=self.bot.main_color,
            timestamp=discord.utils.utcnow()
        )

        avatar = self.bot.user.display_avatar.url if self.bot.user else None

        embed.set_author(
            name="Kairo Hosting - Modmail",
            icon_url=avatar,
        )

        if avatar:
            embed.set_thumbnail(url=avatar)

        embed.description = (
            "This Modmail bot is **hosted and managed** by **Kairo**.\n"
            "It provides a clean and reliable way to communicate with server staff."
        )

        embed.add_field(name="Uptime", value=self.bot.uptime)
        embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f} ms")
        embed.add_field(name="Version", value=f"`{self.bot.version}`")
        embed.add_field(name="Authors", value="`kyb3r`, `Taki`, `fourjr`")

        embed.add_field(
            name="Hosting",
            value=(
                "This bot is hosted by **KAIRO**.\n"
                "For support, join: **https://discord.gg/eATZZpYgps**"
            ),
            inline=False
        )

        embed.add_field(
            name="About Modmail",
            value=(
                "Modmail is an open-source support bot that allows users to "
                "contact staff via DMs in an organised system."
            ),
            inline=False
        )

        embed.set_footer(text="Kairo Modmail • @aexhann")

        await ctx.send(embed=embed)


async def setup(bot):
    removed = bot.remove_command("about")

    if removed is None:
        logger.warning("Could not remove default 'about' command.")

    await bot.add_cog(Branding(bot))
