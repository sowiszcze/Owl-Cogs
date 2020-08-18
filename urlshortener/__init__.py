from .urlshortener import UrlShortener

__red_end_user_data_statement__ = "This cog does not store any user data by itself. Users wanting to remove links from Firebase should contact Support via <https://firebase.google.com/support>."

def setup(bot):
    cog = UrlShortener(bot)
    bot.add_cog(cog)