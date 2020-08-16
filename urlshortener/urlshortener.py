import discord
from redbot.core import commands, checks
from redbot.core.config import Config


class UrlShortener(commands.Cog):
    """
    Allows users to shorten URLs using Firebase provider.
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=872143714,
            force_registration=True,
        )

    @commands.command()
    async def shortenurl(self, ctx):
        """Test command to check if I still can into basic Python"""
        await ctx.send("THIS WORKS!!!!")