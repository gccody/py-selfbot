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
        embed: Embed = Embed(title='Restarting...', colour=0x000000)
        self.bot.webhook.send('client', embed)
        os.execv(sys.executable, ['python'] + sys.argv)

    @command(name="pull")
    async def pull(self, _):
        self.update()

    @staticmethod
    def update():
        g = git.cmd.Git(working_dir=os.getcwd())
        branch = g.execute(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        g.execute(['git', 'fetch', 'origin', branch])
        update = g.execute(['git', 'remote', 'show', 'origin'])
        return not ('up to date' in update or 'fast-forward' in update)




def setup(bot):
    bot.add_cog(Misc(bot))