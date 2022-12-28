from asyncio import sleep

from discord.embeds import Embed
from discord.errors import Forbidden, HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.guild import Guild
from discord.member import Member, User

from lib.bot import Bot
from lib.scraped_user import ScrapedUser


class Scrape(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="scrape", description='Get the data of all of the users in the current guild')
    async def scrape(self, ctx: Context):
        await ctx.message.delete()
        guild: Guild = ctx.guild
        members: list[Member] = guild.members
        embed: Embed = Embed(title=f'Scraping', description=f'Scraping from {guild.name} ({guild.id})', colour=0x00ff00)
        embed.add_field(name='Total Members: ', value=f'`{str(len(members))}`', inline=True)
        embed.add_field(name='Estimated time', value=f'`{str(len(members) * 10)} seconds`', inline=True)
        embed.add_field(name='Wait time between each user (Necessary to prevent api ban)',
                        value=f'{self.bot.config.scrape_delay} seconds', inline=True)
        self.bot.webhook.send('client', embed)
        for member in members:
            # if member.bot: continue
            if member.id == self.bot.user.id: continue
            await sleep(10)
            user: User = member._user
            scraped_user: ScrapedUser = ScrapedUser(user)
            await scraped_user.init()
            self.bot.scraped_users.append(scraped_user)

    @command(name="scrapped_length", aliases=['length', 'slength', 'len', 'slen', 'scrappedlength'], description='Get the amount of users scrapped so far')
    async def scrapped_length(self, ctx: Context):
        await ctx.send(str(len(self.bot.scraped_users)))

    @command(name='dm_scrapped', aliases=['massdm', 'dmscrapped', 'dms'], description='Dm the users that are scrapped so far')
    async def dm_scrapped(self, ctx: Context, *message: str):
        for user in self.bot.scraped_users:
            try:
                await user.dm(" ".join(message))
            except Forbidden:
                embed: Embed = Embed(title=f'Dm\'s with {user.display_name}#{user.discriminator}',
                                     description='Invalid perms to send to this user', colour=0xff0000)
                self.bot.webhook.send('error', embed)
            except HTTPException:
                embed: Embed = Embed(title=f'Dm\'s with {user.display_name}#{user.discriminator}',
                                     description='Message failed to send', colour=0xff0000)
                self.bot.webhook.send('error', embed)


def setup(bot):
    bot.add_cog(Scrape(bot))
