from discord.errors import NotFound, Forbidden, HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context

from lib.bot import Bot


class Message(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="since", aliases=['time', 's'], description='Get the time how long ago a message was sent')
    async def since(self, ctx: Context):
        if ctx.message.reference is None: return
        try:
            msg = await ctx.fetch_message(ctx.message.reference.message_id)
            time = ctx.message.created_at - msg.created_at
            await ctx.message.edit(content=f'{self.bot.utils.humanize(int(time.total_seconds()))}')
        except NotFound:
            await ctx.reply(f'Message was not found')


def setup(bot):
    bot.add_cog(Message(bot))
