import datetime
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.member import Member, Asset, User
import json

from lib.bot import Bot

class Scrape(Cog):
  def __init__(self, bot):
    self.bot: Bot = bot

  @command(name="scrape")
  async def scrape(self, ctx: Context):
    members: list[Member] = ctx.guild.members
    length: int = 0
    for member in members:
      user: User = member._user
      if user.bot: pass
      jsonstr = json.dumps({
        "id": user.id,
        "display_name": user.display_name,
        "discriminator": user.discriminator,
        "icon_url": f"https://cdn.discordapp.com{user.avatar_url_as(format=('gif' if user.is_avatar_animated() else 'png'))._url}",
        "Created At Str": user.created_at.strftime(f"%m/%d/%Y, %I:%M:%S %p"),
        "Created At Timestamp": user.created_at.timestamp()
      }, sort_keys=False, indent=2)
      print(jsonstr)
      length+=1
    print(length)
    
def setup(bot):
  bot.add_cog(Scrape(bot))