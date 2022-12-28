from discord.errors import NotFound, Forbidden, HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.message import Message

from lib.bot import Bot


class Message(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    def format_str(self, amount: int, string: str):
        if amount == 1:
            return string
        return string + 's'

    def humanize(self, time):
        times = []
        times_to_ms = {
            'Year': 3154e7,
            'Month': 2628e6,
            'Week': 604800,
            'Day': 86400,
            'Hour': 3600,
            'Minute': 60,
            'Second': 1
        }
        for i, mod in times_to_ms.items():
            amount, time = divmod(time, mod)
            if amount == 0: continue
            times.append(f'{int(amount)} {self.format_str(amount, i)}')

        return ' '.join(times) + ' ago'

    @command(name="since", aliases=['time', 's'], description='Get the time how long ago a message was sent')
    async def since(self, ctx: Context):
        if ctx.message.reference is None: return
        try:
            msg: Message = await ctx.fetch_message(ctx.message.reference.message_id)
            ctx_msg: Message = ctx.message
            time = ctx_msg.created_at - msg.created_at
            await ctx_msg.edit(content=f'{self.humanize(int(time.total_seconds()))}')
        except NotFound:
            await ctx.reply(f'Message was not found')
        except Forbidden:
            await ctx.reply(f'You don\'t have sufficient perms')
        except HTTPException:
            await ctx.reply(f'Failed for some reason. idk')


def setup(bot):
    bot.add_cog(Message(bot))
