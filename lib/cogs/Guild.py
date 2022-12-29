import re
from lib.bot import Bot
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.guild import Guild, TextChannel


class Gguild(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="+text", aliases=['textchannel'])
    async def add_text_channel(self, ctx: Context, *name: str):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.reply(f"Insufficient perms (Manage Channels)")
        name = ' '.join(name)[:24]
        await ctx.guild.create_text_channel(name=name, category=ctx.channel.category if isinstance(ctx.channel, TextChannel) else None)

    @command(name='+voice', aliases=['voicechannel'])
    async def add_voice_channel(self, ctx: Context, *name: str):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.reply(f"Insufficient perms (Manage Channels)")
        ch: TextChannel
        name = ' '.join(name)[:24]
        await ctx.guild.create_voice_channel(name=name)

    @command(name='+stage', aliases=['stagechannel'])
    async def add_stage_channel(self, ctx: Context, *name: str):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.reply(f"Insufficient perms (Manage Channels)")
        name = ' '.join(name)[:24]
        await ctx.guild.create_stage_channel(name=name, category=ctx.channel.category if isinstance(ctx.channel, TextChannel) else None)

    @command(name='+category', aliases=['category'])
    async def add_category(self, ctx: Context, *name: str):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.reply(f"Insufficient perms (Manage Channels)")
        await ctx.guild.create_category(name=" ".join(name))

    @command(name='-text')
    async def remove_text_channel(self, ctx: Context):
        guild: Guild
        ch: TextChannel
        await ch.delete()
        await ctx.channel


def setup(bot):
    bot.add_cog(Gguild(bot))
