import asyncio

from lib.bot import Bot
from discord.ext.commands import Cog
from discord.ext.commands import command, bot_has_permissions
from discord.ext.commands.context import Context
from discord.guild import Guild, TextChannel
from typing import Optional
from discord.embeds import Embed


class Gguild(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="+text", aliases=['textchannel'])
    @bot_has_permissions(manage_channels=True)
    async def add_text_channel(self, ctx: Context, *name: str):
        name = ' '.join(name)[:24]
        await ctx.guild.create_text_channel(name=name, category=ctx.channel.category if isinstance(ctx.channel, TextChannel) else None)

    @command(name='+voice', aliases=['voicechannel'])
    @bot_has_permissions(manage_channels=True)
    async def add_voice_channel(self, ctx: Context, *name: str):
        ch: TextChannel
        name = ' '.join(name)[:24]
        await ctx.guild.create_voice_channel(name=name)

    @command(name='+stage', aliases=['stagechannel'])
    @bot_has_permissions(manage_channels=True)
    async def add_stage_channel(self, ctx: Context, *name: str):
        name = ' '.join(name)[:24]
        await ctx.guild.create_stage_channel(name=name, category=ctx.channel.category if isinstance(ctx.channel, TextChannel) else None)

    @command(name='+category', aliases=['category'])
    @bot_has_permissions(manage_channels=True)
    async def add_category(self, ctx: Context, *name: str):
        await ctx.guild.create_category(name=" ".join(name))

    @command(name='-text')
    @bot_has_permissions(manage_channels=True)
    async def remove_text_channel(self, ctx: Context):
        await ctx.message.delete()
        await ctx.channel.delete()

    @command(name='guild_delete', aliases=['-guild', 'guilddelete', 'guildelete'])
    async def guild_delete(self, ctx: Context, code: Optional[str]):
        await ctx.message.delete()
        guild: Guild = ctx.guild
        if guild.owner_id != ctx.author.id:
            embed: Embed = Embed(title='Missing Perms', description=f'In order to delete guild you need to be owner of the guild', colour=0xff0000)
            return self.bot.webhook.send('error', embed)
        if not code and self.bot.mfa():
            embed: Embed = Embed(title='Mfa', description=f'In order to delete the guild you need to send the mfa code to delete. Ex: {self.bot.command_prefix}-guild <code>', colour=0xff0000)
            return self.bot.webhook.send('error', embed)
        asyncio.create_task(self.bot.api_helper.remove_guild(guild.id, code))


def setup(bot):
    bot.add_cog(Gguild(bot))
