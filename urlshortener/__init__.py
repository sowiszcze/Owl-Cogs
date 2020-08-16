from .urlshortener import UrlShortener

def setup(bot):
    cog = UrlShortener(bot)
    bot.add_cog(cog)