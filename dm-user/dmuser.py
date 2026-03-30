from __future__ import annotations

i [oai_citation:0‡docs.modmail.dev](https://docs.modmail.dev/usage-guide/plugins?utm_source=chatgpt.com)from discord.ext import commands


class Dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def resolve_user(self, ctx: commands.Context, raw: str) -> discord.User | None:
        """
        Resolve a user from:
        - mention: <@123> / <@!123>
        - plain ID: 123
        - username/tag lookup via discord.py's UserConverter
        """
        raw = raw.strip()

        # Mention or raw ID
        match = re.fullmatch(r"<@!?(\d+)>", raw) or re.fullmatch(r"(\d+)", raw)
        if match:
            user_id = int(match.group(1))
            user = self.bot.get_user(user_id)
            if user is not None:
                return user
            try:
                return await self.bot.fetch_user(user_id)
            except discord.NotFound:
                return None
            except discord.HTTPException:
                return None

        # Fallback to discord.py's converter
        try:
            return await commands.UserConverter().convert(ctx, raw)
        except commands.BadArgument:
            return None

    @commands.command(name="dm")
    @commands.guild_only()
    async def dm(self, ctx: commands.Context, target: str, *, message: str):
        user = await self.resolve_user(ctx, target)

        if user is None:
            await ctx.reply(
                "I couldn't find that user. Use a mention or an ID.",
                mention_author=False,
            )
            return

        embed = discord.Embed(
            description=message,
            colour=discord.Color.blurple(),
        )
        embed.set_footer(text=f"Sent by {ctx.author} ({ctx.author.id})")
        if ctx.author.avatar:
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        else:
            embed.set_author(name=str(ctx.author))

        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            await ctx.reply(
                "I couldn't DM that user.",
                mention_author=False,
            )
            return
        except discord.HTTPException:
            await ctx.reply(
                "Something went wrong while sending the DM.",
                mention_author=False,
            )
            return

        await ctx.reply("dm'ed the user", mention_author=False)


async def setup(bot):
    await bot.add_cog(Dm(bot))
