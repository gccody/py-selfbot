import json

import requests
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context

from lib.bot import Bot


class Self(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="change_discrim")
    async def change_discriminator(self, ctx: Context, discrim: str):
        res, data = self.bot.api_helper.set_username(self.bot.user.name, discrim.strip())
        if res:
            await ctx.reply(f'>>> Discriminator changed to {self.bot.user.name}#{discrim.strip()}')
        else:
            if 'retry_after' in data:
                await ctx.reply(
                    f'You are being rate limited. Retry in {self.bot.utils.humanize(int(data["retry_after"]))}')
            else:
                print(data)
            await ctx.reply('Failed')

    @command(name="change_username")
    async def change_username(self, ctx: Context, username: str):
        res, data = self.bot.api_helper.set_username(username.strip(), self.bot.user.discriminator)
        if res:
            await ctx.reply(f'>>> Username changed to {username.strip()}#{self.bot.user.discriminator}')
        else:
            if 'retry_after' in data:
                await ctx.reply(
                    f'You are being rate limited. Retry in {self.bot.utils.humanize(int(data["retry_after"]))}')
            else:
                print(data)
            await ctx.reply('Failed')

    @command(name="change_email")
    async def change_email(self, ctx: Context, email: str):
        res, data = self.bot.api_helper.change_email(email)
        if res:
            self.bot.config.set('email', email)
            await ctx.reply(f'>>> Email changed to {self.bot.user.email}')
        else:
            if 'retry_after' in data:
                await ctx.reply(
                    f'You are being rate limited. Retry in {self.bot.utils.humanize(int(data["retry_after"]))}')
            else:
                print(data)
            await ctx.reply('Failed')

    @command(name="change_password")
    async def change_password(self, ctx: Context, password: str):
        res, data = self.bot.api_helper.change_password(password)
        if res:
            self.bot.config.set('password', password)
            await ctx.reply(f'>>> Password changed to {self.bot.user.password}')
        else:
            if 'retry_after' in data:
                await ctx.reply(
                    f'You are being rate limited. Retry in {self.bot.utils.humanize(int(data["retry_after"]))}')
            else:
                print(data)
                await ctx.reply('Failed')


def setup(bot):
    bot.add_cog(Self(bot))
