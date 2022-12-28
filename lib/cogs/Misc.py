from lib.bot import Bot
from discord.embeds import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
import subprocess
import git
import os
import sys


class Misc(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="restart", aliases=['rs'], description='Restart the bot')
    async def restart(self, _):
        self.r()

    @command(name="pull", description='Pull from github')
    async def pull(self, _):
        self.u()

    @command(name="update", description='Update the bot if needed')
    async def update(self, ctx: Context):
        await ctx.message.delete()
        if self.u():
            embed: Embed = Embed(title='Updated successfully', colour=0x00ff00)
            self.bot.webhook.send('client', embed)
            self.r()
        else:
            embed: Embed = Embed(title='Already up to date!', colour=0x00ff00)
            self.bot.webhook.send('client', embed)

    @command(name='update_config', aliases=['updateconfig', 'uc', 'set_config', 'setconfig', 'sc'])
    async def update_config(self, ctx: Context, key: str, *value: str):
        await ctx.message.delete()
        value = ' '.join(value)
        if key not in self.bot.config.valid_keys: return await ctx.send('Not a valid key')
        self.bot.config.set(key, value)
        embed: Embed = Embed(title='Config Update', colour=0x00ff00)
        embed.add_field(name=key, value=value, inline=True)
        self.bot.webhook.send('client', embed)

    @command(name='check_config', aliases=['checkconfig', 'cc'])
    async def check_config(self, ctx: Context):
        await ctx.message.delete()
        data = vars(self.bot.config)
        empty = [key for key, val in data.items() if val == '']
        if len(empty) == 0:  embed: Embed = Embed(title='Missing values', description='None', colour=0x00ff00)
        else: embed: Embed = Embed(title='Missing values', description='```\n' + '\n'.join(empty) + ' \n```', colour=0xffff00)
        self.bot.webhook.send('client', embed)

    @staticmethod
    def u():
        repo = git.Repo(os.getcwd())
        curr = repo.head.commit
        repo.remotes.origin.pull()
        return curr != repo.head.commit

    def r(self):
        embed: Embed = Embed(title='Restarting...', colour=0x000000)
        self.bot.webhook.send('client', embed)
        os.execv(sys.executable, ['python'] + sys.argv)


def setup(bot):
    bot.add_cog(Misc(bot))
