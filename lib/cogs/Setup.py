import asyncio
from asyncio import sleep

from discord.abc import GuildChannel
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.guild import Guild
from discord.webhook import Webhook

from lib.bot import Bot


class Setup(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def delete_channel(self, channel_id: str) -> None:
        channel = self.bot.get_channel(int(channel_id))
        if not channel: return
        await channel.delete()
        print(f"Deleted channel {channel.name}")

    async def create_channel(self, guild: Guild, name: str, key: str) -> None:
        channel: TextChannel = await guild.create_text_channel(name=name)
        channel.topic = key
        webhook: Webhook = await channel.create_webhook(name=name)
        self.bot.config.set(key, webhook.url)
        self.bot.webhook.set(key, webhook.url)
        print(f"Created channel {name} and webhook {name}")

    @command(name="setup", description="Only run once on first startup")
    async def setup(self, ctx: Context):
        await ctx.message.delete()
        guild: Guild = await self.bot.create_guild(name="Gccody Selfbot Logging",
                                                   icon=open('./lib/utils/logo.jpg', 'rb').read())
        deleted = []
        self.bot.config.set('guildId', str(guild.id))
        channels = self.bot.api_helper.get_channels(guild.id)
        for channel in channels:
            deleted.append(asyncio.ensure_future(self.delete_channel(channel)))
        await asyncio.gather(*deleted)
        channels: list[str] = ['user-updates', 'client-updates', 'guild-updates', 'errors']
        keys: list[str] = ['user', 'client', 'guild', 'error']
        created = []
        for name, key in zip(channels, keys):
            created.append(asyncio.create_task(self.create_channel(guild, name, key)))

        await asyncio.gather(*created)

        embed: Embed = Embed()
        embed.title = "Guild Created"
        embed.colour = 0x00ff00
        embed.description = "New guild is created and all channels are setup. Ready to run. Ignore Runtime Error in console"

        warning: Embed = Embed()
        warning.title = "Warning"
        warning.colour = 0xff0000
        warning.description = f"DO NOT MODIFY THIS GUILD OR YOU MIGHT BREAK THINGS. IF THINGS ARE BROKEN AND CAN'T BE FIXED THEN YOU HAVE TO DO `{self.bot.command_prefix}setup` ALL OVER AGAIN"

        self.bot.webhook.send('client', embed)
        self.bot.webhook.send('guild', warning)


def setup(bot):
    bot.add_cog(Setup(bot))
