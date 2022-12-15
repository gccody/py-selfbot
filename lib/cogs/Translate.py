from lib.bot import Bot
from googletrans import Translator
from discord.ext.commands import Cog
from discord.message import Message, Embed
from discord.ext.commands import command
from discord.ext.commands.context import Context

class Translate(Cog):
  def __init__(self, bot):
    self.bot: Bot = bot

  @command(name="translate", aliases=['trans', 't'])
  async def translate(self, ctx: Context, lang: str, *message: str):
    t = Translator(raise_exception=False)
    res = t.translate(" ".join(message), lang)
    await ctx.send(res.text)
    
  @translate.error
  async def translate_error(self, ctx: Context, exc):
    if 'lang is a required argument that is missing.' in exc or 'invalid destination language' in exc:
      embed: Embed(title="Invalid Language", colour=0xff0000)
      embed.description = f"""
Input:
`{ctx.message.content}`
Expected (EXAMPLE):
`.translate es Hello World This is translated to Spanish!`
"""
      await self.bot.webhook.send('error', embed)

def setup(bot):
  bot.add_cog(Translate(bot))