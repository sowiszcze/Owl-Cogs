import discord
import requests
import validators
from redbot.core import commands, checks
from redbot.core.config import Config
from typing import Literal

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
        self.config.register_guild(
            prefix=None
        )

    @commands.group()
    @commands.guild_only()
    @checks.admin_or_permissions()
    async def shortenurlset(self, ctx: commands.Context):
        """Configure UrlShortener."""
        pass

    @shortenurlset.command(name="prefix")
    async def set_prefix(self, ctx: commands.Context, prefix: str):
        """Set domain URI prefix."""
        await self.config.guild(ctx.guild).prefix.set(prefix)
        await ctx.send("Domain URI prefix was set!")

    @commands.command()
    @commands.guild_only()
    @checks.mod()
    @checks.bot_has_permissions(embed_links=True)
    async def shortenurl(self, ctx: commands.Context, url: str, option: str = "UNGUESSABLE"):
        """Shorten URL using Firebase.
        
        `option` can be set to:
        - `SHORT` to generate path strings that are only as long as needed to be unique, with a minimum length of 4 characters. Use this method if sensitive information would not be exposed if a short Dynamic Link URL were guessed.
        - `UNGUESSABLE` to shorten the path to an unguessable string. Such strings are created by base62-encoding randomly generated 96-bit numbers, and consist of 17 alphanumeric characters. Use unguessable strings to prevent your Dynamic Links from being crawled, which can potentially expose sensitive information."""

        if not validators.url(url):
            return await ctx.send("You haven't provided a valid URL.")

        option = option.upper()
        if option != "UNGUESSABLE" and option != "SHORT":
            return await ctx.send("`option` should be either `SHORT` or `UNGUESSABLE`.")

        firebase_keys = await self.bot.get_shared_api_tokens("firebase")
        if firebase_keys.get("api_key") is None:
            return await ctx.send("The Firebase API key has not been set. Set it with `>set api firebase api_key,<your_api_key>`.")

        prefix = await self.config.guild(ctx.guild).prefix()
        if prefix is None:
            return await ctx.send("Domain URI prefix is not set. Set it with `>shortenurlset prefix <your_prefix>`.")
        
        endpoint = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=" + firebase_keys.get("api_key")
        payload = { "dynamicLinkInfo": { "domainUriPrefix": prefix, "link": url }, "suffix": { "option": option }}
        
        r = requests.post(endpoint, json=payload)
        if r.status_code != requests.codes.ok:
            await ctx.send("Firebase API returned error code " + r.status_code + "\nI'll try to embed error message below.")
            embed = discord.Embed(
                title="\N{CROSS MARK} Firebase API returned error code " + r.status_code,
                description=(r.json()["error"]["message"]),
                color=await ctx.embed_color()
            )
            return await ctx.send(embed=embed)

        info = r.json()
        embed = discord.Embed(
            title="\N{WHITE HEAVY CHECK MARK} URL succesfully shortened",
            description=("Short link: [{0}]({0})\nPreview link: [{1}]({1})".format(info["shortLink"], info["previewLink"])),
            color=await ctx.embed_color()
        )
        if ctx.author.id == ctx.guild.owner_id and not info["warning"] is None:
            for warning in info["warning"]:
                embed.add_field(
                    name="\N{WARNING SIGN} {}".format(warning["warningCode"]),
                    value=warning["warningMessage"],
                    inline=False
                )
        return await ctx.send(embed=embed)

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        """
            Method for finding users data inside the cog and deleting it.
        """
        pass