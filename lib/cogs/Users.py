import re
from lib.bot import Bot
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.message import Message
from discord.user import User
from discord.member import Member
from discord.user import ClientUser
from lib.scraped_user import ScrapedUser


class Users(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="info", aliases=['whois'])
    async def info(self, ctx: Context, _):
        msg: Message = ctx.message
        for member in msg.mentions:
            member: Member
            if type(member._user) is ClientUser:
                u: ClientUser = member._user
                m = f""">>> 
{u.display_name}#{u.discriminator} ({u.id})

Created At: `{u.created_at.strftime(f"%m/%d/%Y, %I:%M:%S %p")}`
"""
                await ctx.reply(m)
                continue

            user: ScrapedUser = ScrapedUser(member._user)
            await user.init()
            m = f""">>> 
{user.display_name}#{user.discriminator} ({user.id})

Created At: `{user.created_at_str}`
Is Your Friend: `{user.is_friend}`
Is Blocked: `{user.is_blocked}`
Premium Since: `{member.premium_since}`
Nitro: `{user.nitro}`
"""
        await ctx.reply(m)

    @command(name='ban', aliases=['b'])
    async def ban(self, ctx: Context, *reason: str):
        if not bool(ctx.author.guild_permissions.ban_members):
            return await ctx.send(""">>> \nInvalid Permissions (Ban Members)""")
        reason = re.sub(r'<@\d+>', "", " ".join(reason)).strip()
        m = ">>> Successfully banned users: \n"
        for member in ctx.message.mentions:
            if type(member._user) is ClientUser: continue
            await member.ban(reason=reason)
            user: User = await self.bot.fetch_user(member._user.id)
            m += f"{user.display_name}#{user.discriminator} ({user.id})\n"

        await ctx.reply(m)

    @command(name='kick', aliases=['k'])
    async def kick(self, ctx: Context, *reason: str):
        if not bool(ctx.author.guild_permissions.kick_members):
            return await ctx.send(""">>> \nInvalid Permissions (Kick Members)""")
        reason = re.sub(r'<@\d+>', "", " ".join(reason)).strip()
        m = ">>> Successfully kicked users: \n"
        for member in ctx.message.mentions:
            if type(member._user) is ClientUser: continue
            await member.kick(reason=reason)
            user: User = await self.bot.fetch_user(member._user.id)
            m += f"{user.display_name}#{user.discriminator} ({user.id})\n"

        await ctx.reply(m)


def setup(bot):
    bot.add_cog(Users(bot))