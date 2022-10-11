import asyncio
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
  
  async def createChannel(self, guild: Guild, name: str, configFunc, webhookFunc) -> None:
    channel: TextChannel = await guild.create_text_channel(name=name)
    webhook: Webhook = await channel.create_webhook(name=name)
    configFunc(webhook.url)
    webhookFunc(webhook.url)
    print(f"Created channel {channel.name} and webhook {webhook.name}")

  @command(name="setup", description="Only run once on first startup")
  async def setup(self, ctx: Context):
    guildId = (await self.bot.create_guild(name="Gccody Selfbot Logging", icon=open('./lib/utils/logo.jpg', 'rb').read())).id
    for guild in self.bot.guilds:
      guild: Guild = guild
      if not guild.id == guildId: continue
      new_guild = guild
      for channel in new_guild.channels:
        asyncio.ensure_future(self.deleteChannel(channel))
      break
    channels: list[dict] = [
      {
        "name": "user-updates",
        "configfunc": self.bot.config.setUserWebhookUrl,
        "webhookfunc": self.bot.webhook.setUser,
      },
      {
        "name": "client-updates",
        "configfunc": self.bot.config.setClientWebhookUrl,
        "webhookfunc": self.bot.webhook.setClient,
      },
      {
        "name": "guild-updates",
        "configfunc": self.bot.config.setGuildWebhookUrl,
        "webhookfunc": self.bot.webhook.setGuild,
      },
      {
        "name": "unhandled-errors",
        "configfunc": self.bot.config.setErrorWebhookUrl,
        "webhookfunc": self.bot.webhook.setError,
      },
    ]
    for channel in channels:
      asyncio.ensure_future(self.createChannel(new_guild, channel["name"], channel["configfunc"], channel["webhookfunc"]))
    embed: Embed = Embed()
    embed.title = "Guild Created"
    embed.colour = 0x00ff00
    embed.description = "New guild is created and all channels are setup. Ready to run. Ignore Runtime Error in console"
    self.bot.webhook.sendClientWebhook()


def setup(bot):
  bot.add_cog(Setup(bot))