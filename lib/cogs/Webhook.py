from typing import Any

from discord import RequestsWebhookAdapter
from discord.channel import TextChannel
from discord.errors import Forbidden, HTTPException, InvalidArgument, NotFound
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.webhook import Webhook

from lib.bot import Bot


class WebhookCreate(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="whcreate", aliases=['whc'])
    async def whcreate(self, ctx: Context, name: str = 'Made by Gccody'):
        channel: TextChannel | Any = ctx.channel
        if not isinstance(channel, TextChannel): return await ctx.reply('Not a viable channel for webhooks')
        try:
            wh: Webhook = await channel.create_webhook(name=name)
        except Forbidden:
            return await ctx.reply('Invalid Permissions')
        except HTTPException:
            return await ctx.reply('Creating the webhook failed')
        await ctx.reply(f'Webhook created: \n > {wh.url}')

    @command(name='whdelete', aliases=['whd'])
    async def whdelete(self, ctx: Context, identify: str):
        channel: TextChannel | Any = ctx.channel
        if not isinstance(channel, TextChannel): return await ctx.reply('Not a viable channel for webhooks')
        whs: list[Webhook] = await channel.webhooks()
        for wh in whs:
            if 'https://discord.com/api/webhooks/' in identify:
                if wh.url == identify:
                    await wh.delete()
                    await ctx.reply(f'Deleted {wh.name}')
                    continue
            else:
                if wh.id == identify:
                    await wh.delete()
                    await ctx.reply(f'Deleted {wh.name}')
                    continue
            if wh.name == identify:
                await wh.delete()
                await ctx.reply(f'Delted {wh.name}')

    @command(name='whsend', aliases=['whs'])
    async def whsend(self, ctx: Context, url: str, amount: int, *message: str):
        try:
            wh: Webhook = Webhook.from_url(url=url, adapter=RequestsWebhookAdapter())
        except InvalidArgument:
            return await ctx.reply('Webhook is invalid')

        for _ in range(amount):
            try:
                await wh.send(message)
            except Forbidden:
                return await ctx.reply('Authorization token incorrect')
            except NotFound:
                return await ctx.reply('Webhook was not found')
            except HTTPException:
                await ctx.reply('Message failed to send')


def setup(bot):
    bot.add_cog(WebhookCreate(bot))
