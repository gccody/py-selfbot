from discord.embeds import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.message import Message
from googletrans import Translator

from lib.bot import Bot


class Translate(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    def get_lang(self, lang: str | None):
        return lang if type(lang) is str else self.bot.config.default_language

    @command(name="translate", aliases=['trans', 't'], description='Reply to a message to translate or translate your own message')
    async def translate(self, ctx: Context, lang: str = None, *message: str):
        t = Translator(raise_exception=False)
        if ctx.message.reference:
            msg: Message = await ctx.fetch_message(ctx.message.reference.message_id)
            ctx_msg: Message = ctx.message
            lang = self.get_lang(lang)
            res = t.translate(msg.content, lang)
            return await ctx_msg.edit(content=res.text)
        await ctx.message.delete()
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
