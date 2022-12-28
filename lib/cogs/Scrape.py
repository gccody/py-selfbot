from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.channel import DMChannel
from discord.member import User

from lib.bot import Bot


class Scrape(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="scrape", description='Get the data of all of the users in the current guild')
    async def scrape(self, ctx: Context):
        await ctx.message.delete()

        for member in ctx.guild.members:
            if member.bot: continue
            self.bot.db.add_user(member.id)

    @command(name="scrapped_length", aliases=['length', 'slength', 'len', 'slen', 'scrappedlength'], description='Get the amount of users scrapped so far')
    async def scrapped_length(self, ctx: Context):
        await ctx.send(str(len(self.bot.db.records('SELECT * FROM users'))))

    @command(name='dm_scrapped', aliases=['massdm', 'dmscrapped', 'dms'], description='Dm the users that are scrapped so far')
    async def dm_scrapped(self, ctx: Context, *message):
        ids = self.bot.db.records('SELECT * FROM users')
        for id, whitelist in ids:
            if bool(whitelist): continue
            user: User = await self.bot.fetch_user(int(id))
            dm_channel: DMChannel = await user.create_dm()
            await dm_channel.send(content=' '.join(message))


def setup(bot):
    bot.add_cog(Scrape(bot))
