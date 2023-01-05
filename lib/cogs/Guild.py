import asyncio

from lib.bot import Bot
from discord.ext.commands import Cog
from discord.ext.commands import command, bot_has_permissions
from discord.ext.commands.context import Context
from discord.guild import Guild, TextChannel
from typing import Optional
from discord.embeds import Embed
from discord.member import Member
import discum


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

    def close_after_fetching(self, client, guild_id):
        if client.gateway.finishedMemberFetching(guild_id):
            lenmembersfetched = len(client.gateway.session.guild(guild_id).members)
            print(str(lenmembersfetched) + ' members fetched')
            client.gateway.removeCommand({'function': self.close_after_fetching, 'params': {'guild_id': guild_id}})
            client.gateway.close()

    def get_members(self, client, guild_id, channel_id):
        client.gateway.fetchMembers(guild_id, channel_id, keep='all')
        client.gateway.command({'function': self.close_after_fetching, 'params': {'guild_id': guild_id}})
        client.gateway.run()
        client.gateway.resetSession()
        return client.gateway.session.guild(guild_id).members

    # @command(name='scrape_guild', aliases=['sg'])
    # async def scrape_guild(self, ctx: Context, *guilds: str):
    #     print("Scrape starting")
    #     await ctx.message.delete()
    #     self.bot.config.set('auto_scrape', False)
    #     # client = discum.Client(token=self.bot.config.token, log=False)
    #     for g_id in guilds:
    #         guild: Guild = self.bot.get_guild(int(g_id))
    #         if not guild: continue
    #         if guild.large:
    #             print('Large guild')
    #             print("Subscribing")
    #             res = await guild.subscribe()
    #             if not res:
    #                 print("Failed to subscribe")
    #                 continue
    #         else:
    #             print("Small guild")
    #         print(f"Scraping from {guild.name}")
    #         print(len(guild.members))
    #
    #     self.bot.config.set('auto_scrape', True)



def setup(bot):
    bot.add_cog(Gguild(bot))
