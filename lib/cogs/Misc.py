from lib.bot import Bot
from discord.embeds import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
import git
import os
import sys


class Misc(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="restart", aliases=['rs'])
    async def restart(self, _):
        self.r()

    @command(name="pull")
    async def pull(self, _):
        self.u()

    @command(name="update")
    async def update(self, _):
        self.u()
        self.r()

    @staticmethod
    def u():
        g = git.cmd.Git(working_dir=os.getcwd())
        g.execute(['git', 'pull'])

    def r(self):
        embed: Embed = Embed(title='Restarting...', colour=0x000000)
        self.bot.webhook.send('client', embed)
        os.execv(sys.executable, ['python'] + sys.argv)






def setup(bot):
    bot.add_cog(Misc(bot))