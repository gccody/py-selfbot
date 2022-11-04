import asyncio
from time import sleep
from lib.bot import Bot
from discord.channel import TextChannel
from discord.webhook import Webhook
from discord.guild import Guild
from discord.embeds import Embed
from discord.abc import GuildChannel
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context

class Setup(Cog):
  def __init__(self, bot):
    self.bot: Bot = bot

  async def deleteChannel(self, channel: GuildChannel) -> None:
    await channel.delete()
    print(f"Deleted channel {channel.name}")
  
  async def createChannel(self, guild: Guild, name: str, key: str) -> None:
    channel: TextChannel = await guild.create_text_channel(name=name)
    channel.topic = key
    webhook: Webhook = await channel.create_webhook(name=name)
    self.bot.config.set(key, webhook.url)
    self.bot.webhook.set(key, webhook.url)
    print(f"Created channel {name} and webhook {name}")

  @command(name="setup", description="Only run once on first startup")
  async def setup(self, ctx: Context):
    guild: Guild = await self.bot.create_guild(name="Gccody Selfbot Logging", icon=open('./lib/utils/logo.jpg', 'rb').read())
    self.bot.config.set('guildId', str(guild.id))
    for channel in guild.channels:
      asyncio.ensure_future(self.deleteChannel(channel))
    channels: list[str] = ['user-updates', 'client-updates', 'guild-updates', 'unhandled-errors']
    keys: list[str] = ['user', 'client', 'guild', 'error']
    for name, key in zip(channels, keys):
      asyncio.ensure_future(self.createChannel(guild, name, key))
    
    embed: Embed = Embed()
    embed.title = "Guild Created"
    embed.colour = 0x00ff00
    embed.description = "New guild is created and all channels are setup. Ready to run. Ignore Runtime Error in console"

    warning: Embed = Embed()
    embed.title = "Warning"
    embed.color = 0xff0000
    embed.description = "DO NOT MODIFY THIS GUILD OR YOU MIGHT BREAK THINGS. IF THINGS ARE BROKEN AND CAN'T BE FIXED THEN YOU HAVE TO DO `.setup\` ALL OVER AGAIN"

    sleep(5)
    self.bot.webhook.send('client', embed)
    self.bot.webhook.send('guild', warning)


def setup(bot):
  bot.add_cog(Setup(bot))