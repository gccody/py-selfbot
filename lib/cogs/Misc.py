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
    async def update(self, ctx: Context):
        await ctx.message.delete()
        if self.u():
            embed: Embed = Embed(title='Updated successfully', colour=0x00ff00)
            self.bot.webhook.send('client', embed)
            self.r()
        else:
            embed: Embed = Embed(title='Already up to date!', colour=0x00ff00)
            self.bot.webhook.send('client', embed)

    @command(name="test")
    async def test(self, _):
        repo = git.Repo(os.getcwd())
        print("Diff?")
        print(repo.head.commit.diff())

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