from typing import Any
from lib.bot import Bot
from discord.channel import TextChannel
from discord.permissions import Permissions
from discord.webhook import Webhook
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.errors import Forbidden, HTTPException
from discord.ext.commands.context import Context

class WebhookCreate(Cog):
  def __init__(self, bot):
    self.bot: Bot = bot

  @command(name="whcreate", aliases=['whc'])
  async def whcreate(self, ctx: Context, name: str = 'Made by Gccody'):
    channel: TextChannel | Any = ctx.channel
    if not isinstance(channel, TextChannel): return await ctx.send('Not a viable channel for webhooks')
    try:
      wh: Webhook = await channel.create_webhook(name=name)
    except Forbidden:
      return await ctx.send('Invalid Permissions')
    except HTTPException:
      return await ctx.send('Creating the webhook failed')
    await ctx.send(f'Webhook created: \n > {wh.url}')

  @command(name='whdelete', aliases=['whd'])
  async def whdelete(self, ctx: Context, identify: str):
    channel: TextChannel | Any = ctx.channel
    if not isinstance(channel, TextChannel): return await ctx.send('Not a viable channel for webhooks')
    whs: list[Webhook] = await channel.webhooks()
    for wh in whs:
      if 'https://discord.com/api/webhooks/' in identify:
        if wh.url == identify:
          await wh.delete()
          await ctx.send(f'Deleted {wh.name}')
          continue
      else:
        if wh.id == identify:
          await wh.delete()
          await ctx.send(f'Deleted {wh.name}')
          continue
      if wh.name == identify:
        await wh.delete()
        await ctx.send(f'Delted {wh.name}')
    
def setup(bot):
  bot.add_cog(WebhookCreate(bot))