import re
from lib.bot import Bot
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.message import Message
from discord.user import User
from discord.member import Member
from discord.role import Role
from discord.user import ClientUser
from discord.guild import Guild
from discord.errors import HTTPException
from discord.permissions import Permissions
from lib.scraped_user import ScrapedUser


class Users(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="info", aliases=['whois'])
    async def info(self, ctx: Context, _):
        msg: Message = ctx.message
        for member in msg.mentions:
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
        auth = ctx.author
        if not bool(ctx.author.guild_permissions.kick_members):
            return await ctx.send(""">>> \nInvalid Permissions (Kick Members)""")
        reason = re.sub(r'<@\d+>', "", " ".join(reason)).strip()
        m = ">>> Successfully kicked users: \n"
        for member in ctx.message.mentions:
            if type(member._user) is ClientUser: continue
            await member.kick(reason=reason)
            mem: Member
            user: User = await self.bot.fetch_user(member._user.id)
            m += f"{user.display_name}#{user.discriminator} ({user.id})\n"

        await ctx.reply(m)

    @command(name='add_role', aliases=['+role', 'addrole', '+r'])
    async def add_role(self, ctx: Context, _):
        if not bool(ctx.author.guild_permissions.manage_roles):
            return await ctx.send(">>> Invalid Permissions (Manage Roles)")
        if len(ctx.message.mentions) == 0:
            return await ctx.send(f">>> Mention users to add the roles to")
        matches = re.finditer(r"<@&(\d+?)>", ctx.message.content, re.MULTILINE)
        guild: Guild = ctx.guild
        valid = []
        invalid = []
        for match in matches:
            role: Role = guild.get_role(int(match.group(1)))
            print(role.position, ctx.author.top_role.position)
            if role.position < ctx.author.top_role.position or ctx.author.id == guild.owner_id:
                valid.append(role)
            else:
                invalid.append(f"<@&{role.id}>")

        if len(invalid) > 0:
            invalid_str = "\n".join(invalid)
            await ctx.reply(f">>> Invalid Roles: {invalid_str}")

        if len(valid) == 0: return

        success_member = []
        success_role = [f"<@&{role.id}>" for role in valid]
        print(valid)
        for member in ctx.message.mentions:
            try:
                await member.add_roles(*valid)
                success_member.append(member.mention)
            except HTTPException:
                await ctx.send(f'Failed applying roles to {member.mention}')

        success_member = " ".join(success_member)
        success_role = "\n".join(success_role)
        await ctx.reply(f"The member(s) ({success_member}) have received the following roles: \n{success_role}")

    @command(name="remove_role", aliases=['-role', '-r', 'removerole'])
    async def remove_role(self, ctx: Context, _):
        if not bool(ctx.author.guild_permissions.manage_roles):
            return await ctx.send(">>> Invalid Permissions (Manage Roles)")
        if len(ctx.message.mentions) == 0:
            return await ctx.send(f">>> Mention users to add the roles to")
        matches = re.finditer(r"<@&(\d+?)>", ctx.message.content, re.MULTILINE)
        guild: Guild = ctx.guild
        valid = []
        invalid = []
        for match in matches:
            role: Role = guild.get_role(int(match.group(1)))
            print(role.position, ctx.author.top_role.position)
            mem: Member
            if role.position < ctx.author.top_role.position or ctx.author.id == guild.owner_id:
                valid.append(role)
            else:
                invalid.append(f"<@&{role.id}>")

        if len(invalid) > 0:
            invalid_str = "\n".join(invalid)
            await ctx.reply(f">>> Invalid Roles: {invalid_str}")

        if len(valid) == 0: return

        success_member = []
        success_role = [f"<@&{role.id}>" for role in valid]
        print(valid)
        for member in ctx.message.mentions:
            try:
                await member.remove_roles(*valid)
                success_member.append(member.mention)
            except HTTPException:
                await ctx.send(f'Failed to remove roles from {member.mention}')

        success_member = " ".join(success_member)
        success_role = "\n".join(success_role)
        await ctx.reply(f"The member(s) ({success_member}) had the following roles removed: \n{success_role}")




def setup(bot):
    bot.add_cog(Users(bot))