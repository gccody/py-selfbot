from concurrent.futures import ThreadPoolExecutor
import math
import asyncio
import threading
from lib.bot import Bot
from itertools import islice
from discord.ext.commands import Cog
from discord.member import Member, User
from lib.scraped_user import ScrapedUser
from discord.ext.commands import command
from discord.ext.commands.context import Context

class Scrape(Cog):
  def __init__(self, bot):
    self.bot: Bot = bot
    self.ex = ThreadPoolExecutor(self.bot.config.threads)

  @command(name="scrape")
  async def scrape(self, ctx: Context):
    members: list[Member] = ctx.guild.members
    print("Scraping...")
    for member in members:
      # if member.bot: continue
      if member.id == self.bot.user.id: continue
      user: User = member._user
      scraped_user: ScrapedUser = ScrapedUser(user)
      await scraped_user.init()
      self.bot.scraped_users.append(scraped_user)
      print(scraped_user.toJsonStr())
    print("Scraped")

  @command(name="scrapped_length", aliases=['length', 'slength', 'len'])
  async def scrapped_length(self, ctx: Context):
    await ctx.send(len(self.bot.scraped_users))

    
def setup(bot):
  bot.add_cog(Scrape(bot))