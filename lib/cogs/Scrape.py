from concurrent.futures import ThreadPoolExecutor

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.member import Member, User
from discord.embeds import Embed
from discord.guild import Guild
from asyncio import sleep

from lib.bot import Bot
from lib.scraped_user import ScrapedUser


class Scrape(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="scrape")
    async def scrape(self, ctx: Context):
        await ctx.message.delete()
        guild: Guild = ctx.guild
        members: list[Member] = guild.members
        embed: Embed = Embed(title=f'Scraping', description=f'Scraping from {guild.name} ({guild.id})', colour=0x00ff00)
        embed.add_field(name='Total Members: ', value=f'`{str(len(members))}`', inline=True)
        embed.add_field(name='Estimated time', value=f'`{str(len(members) * 10)} seconds`', inline=True)
        self.bot.webhook.send('client', embed)
        for member in members:
            # if member.bot: continue
            if member.id == self.bot.user.id: continue
            await sleep(10)
            user: User = member._user
            scraped_user: ScrapedUser = ScrapedUser(user)
            await scraped_user.init()
            self.bot.scraped_users.append(scraped_user)
            print(scraped_user.to_json_str())

        print("Scraped")

    @command(name="scrapped_length", aliases=['length', 'slength', 'len', 'slen', 'scrappedlength'])
    async def scrapped_length(self, ctx: Context):
        await ctx.send(str(len(self.bot.scraped_users)))


def setup(bot):
    bot.add_cog(Scrape(bot))
