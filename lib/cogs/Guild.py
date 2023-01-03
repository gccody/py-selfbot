from lib.bot import Bot
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.guild import Guild, TextChannel
from typing import Optional
from discord.embeds import Embed


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
        await ctx.channel.delete()

    @command(name='guild_delete', aliases=['-guild', 'guilddelete', 'guildelete'])
    async def guild_delete(self, ctx: Context, code: Optional[str]):
        await ctx.message.delete()
        if not code and self.bot.mfa():
            embed: Embed = Embed(title='Mfa', description=f'In order to delete the guild you need to send the mfa code to delete. Ex: {self.bot.command_prefix}-guild <code>', colour=0xff0000)
            self.bot.webhook.send('error', embed)
        guild: Guild = ctx.guild
        if guild.owner_id != ctx.author.id:
            embed: Embed = Embed(title='Missing Perms', description=f'In order to delete guild you need to be owner of the guild', colour=0xff0000)
            self.bot.webhook.send('error', embed)
        return self.bot.api_helper.remove_guild(guild.id, code)

    @guild_delete.error
    async def guild_delete_error(self, ctx, exc):
        pass


def setup(bot):
    bot.add_cog(Gguild(bot))
