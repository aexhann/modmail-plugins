from discord.ext import commands
import discord
import re


class Dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def resolve_user(self, ctx, raw: str):
        raw = raw.strip()

        # Check mention or ID
        match = re.fullmatch(r"<@!?(\d+)>", raw) or re.fullmatch(r"(\d+)", raw)
        if match:
            user_id = int(match.group(1))
            user = self.bot.get_user(user_id)
            if user:
                return user
            try:
                return await self.bot.fetch_user(user_id)
            except:
                return None

        # Fallback converter
        try:
            return await commands.UserConverter().convert(ctx, raw)
        except:
            return None

    @commands.command(name="dm")
    async def dm(self, ctx, target: str, *, message: str):
        user = await self.resolve_user(ctx, target)

        if not user:
            return await ctx.send("Couldn't find that user.")

        embed = discord.Embed(
            description=message,
            colour=discord.Color.blurple()
        )
        embed.set_footer(text=f"Sent by {ctx.author}")

        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            return await ctx.send("Can't DM that user.")

        await ctx.send("dm'ed the user")


async def setup(bot):
    await bot.add_cog(Dm(bot))
