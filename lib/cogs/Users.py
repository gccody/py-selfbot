import re
from lib.bot import Bot
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.message import Message
from discord.embeds import Embed
from discord.user import User
from discord.member import Member
from discord.role import Role
from discord.user import ClientUser
from discord.guild import Guild
from discord.errors import HTTPException, Forbidden
from lib.scraped_user import ScrapedUser
from discord.permissions import Permissions
from discum.utils.slash import SlashCommander


class Users(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(name="info", aliases=['whois'], description='Look up the details of a certain user')
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
Joined At: `{member.joined_at.strftime(f"%m/%d/%Y, %I:%M:%S %p")}`
Bot?: `{member.bot}`
Top Role: `{member.top_role.mention}`
Status: `{str(member.status).title()}`
Activity: `{str(member.activity.type).split(".")[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''}`
Is Your Friend: `{user.is_friend}`
Is Blocked: `{user.is_blocked}`
Boosted: `{member.premium_since}`
Nitro: `{user.nitro}`
"""
            await ctx.reply(m)

    @command(name='ban', aliases=['b'], description='Ban a user or multiple users')
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

    @command(name='hackban')
    async def hack_ban(self, ctx: Context, *reason: str):
        if not bool(ctx.author.guild_permissions.ban_members):
            return await ctx.send(""">>> \nInvalid Permissions (Ban Members)""")
        ids = re.findall(r'\d{17,19}', " ".join(reason))
        reason = re.sub(r'\d{17,19}', "", " ".join(reason)).strip()
        guild: Guild = ctx.guild
        for id in ids:
            await guild.ban(self.bot.get_user(id=(int(id))), reason=reason)

        await ctx.reply(f'>>> Banned {len(ids)} members')

    @command(name='kick', aliases=['k'], description='Kick a user or multiple users')
    async def kick(self, ctx: Context, *reason: str):
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

    @command(name='+timeout', description='Timeout a user or multiple users')
    async def add_timeout(self, ctx: Context, minutes: int, *reason: str):
        print('Starting timeout')
        if not bool(ctx.author.guild_permissions.mute_members):
            return await ctx.send(""">>> \nInvalid Permissions (Mute Members)""")
        reason = re.sub(r'<@\d+>', "", " ".join(reason)).strip()
        success = []
        failed = []
        new = "\n"
        for member in ctx.message.mentions:
            print(member.id)
            res = self.bot.api_helper.timeout_user(str(member.id), str(ctx.guild.id), minutes, reason)
            print(res)
            if res:
                success.append(member.mention)
            else:
                failed.append(member.mention)

        if len(success) > 0: await ctx.reply(f'Successfully timed out: >>> {new.join(success)}')
        if len(failed) > 0: await ctx.reply(f'Failed to timeout: >>> {new.join(failed)}')

    @command(name='-timeout', description='Un-timeout a user or multiple users')
    async def remove_timeout(self, ctx: Context, _):
        perm: Permissions
        if not bool(ctx.author.guild_permissions.mute_members):
            return await ctx.send(""">>> \nInvalid Permissions (Mute Members)""")
        success = []
        failed = []
        new = "\n"
        for member in ctx.message.mentions:
            mem: Member
            res = self.bot.api_helper.remove_timeout(str(member.id), str(ctx.guild.id))
            print(res)
            if res:
                success.append(member.mention)
            else:
                failed.append(member.mention)

        if len(success) > 0: await ctx.reply(f'Successfully removed timed out: >>> {new.join(success)}')
        if len(failed) > 0: await ctx.reply(f'Failed to remove timeout: >>> {new.join(failed)}')

    @command(name='add_role', aliases=['+role', 'addrole', '+r'],
             description='Add a role or multiple roles to a user or multiple users')
    async def add_role(self, ctx: Context, _):
        if not bool(ctx.author.guild_permissions.manage_roles):
            return await ctx.send(">>> Invalid Permissions (Manage Roles)")
        if len(ctx.message.mentions) == 0:
            return await ctx.send(f">>> Mention users to add the roles to")
        matches = re.finditer(r"<@&(\d+?)>", ctx.message.content, re.MULTILINE)
        guild: Guild = ctx.guild
        valid = []
        invalid = []
        new = "\n"
        for match in matches:
            role: Role = guild.get_role(int(match.group(1)))
            print(role.position, ctx.author.top_role.position)
            if role.position < ctx.author.top_role.position or ctx.author.id == guild.owner_id:
                valid.append(role)
            else:
                invalid.append(f"<@&{role.id}>")

        if len(invalid) > 0:
            await ctx.reply(f">>> Invalid Roles: {new.join(invalid)}")

        if len(valid) == 0: return

        success_member = []
        success_role = [f"<@&{role.id}>" for role in valid]
        for member in ctx.message.mentions:
            try:
                await member.add_roles(*valid)
                success_member.append(member.mention)
            except HTTPException:
                await ctx.send(f'Failed applying roles to {member.mention}')

        success_member = " ".join(success_member)
        success_role = "\n".join(success_role)
        await ctx.reply(f"The member(s) ({success_member}) have received the following roles: \n{success_role}")

    @command(name="remove_role", aliases=['-role', '-r', 'removerole'],
             description='Remove a role or multiple roles from a user or multiple users')
    async def remove_role(self, ctx: Context, _):
        if not bool(ctx.author.guild_permissions.manage_roles):
            return await ctx.send(">>> Invalid Permissions (Manage Roles)")
        if len(ctx.message.mentions) == 0:
            return await ctx.send(f">>> Mention users to remove the roles from")
        matches = re.findall(r"<@&(\d+?)>", ctx.message.content, re.MULTILINE)
        guild: Guild = ctx.guild
        valid = []
        invalid = []
        new = "\n"
        for id in matches:
            role: Role = guild.get_role(int(id))
            mem: Member
            if role.position < ctx.author.top_role.position or ctx.author.id == guild.owner_id:
                valid.append(role)
            else:
                invalid.append(f"<@&{role.id}>")

        if len(invalid) > 0:
            await ctx.reply(f">>> Invalid Roles: {new.join(invalid)}")

        if len(valid) == 0: return

        success_member = []
        success_role = [f"<@&{role.id}>" for role in valid]
        for member in ctx.message.mentions:
            try:
                await member.remove_roles(*valid)
                success_member.append(member.mention)
            except HTTPException:
                await ctx.send(f'Failed to remove roles from {member.mention}')

        success_member = " ".join(success_member)
        success_role = "\n".join(success_role)
        await ctx.reply(f"The member(s) ({success_member}) had the following roles removed: \n{success_role}")

    @command(name="add_friend", aliases=['+friend', 'addfriend', '+f'],
             description='Send a friend request to a user or multiple users')
    async def add_friend(self, ctx: Context, _):
        if len(ctx.message.mentions) == 0:
            return await ctx.send(f">>> Mention users to send friend requests")

        success = []
        failed = []
        for member in ctx.message.mentions:
            if member._user.id == self.bot.user.id: continue
            try:
                await member.send_friend_request()
                success.append(member.mention + f' ({member._user.id})')
            except Forbidden:
                failed.append(member.mention + f' ({member._user.id})')

            if len(failed) > 0:
                failed_str = '\n'.join(failed)
                await ctx.reply(f"Failed to send request(s) to: >>>\n{failed_str}")

            if len(success) > 0:
                success_str = '\n'.join(success)
                await ctx.reply(f'Sent request(s) to: >>>\n{success_str}')

    @command(name='+whitelist')
    async def add_whitelist(self, ctx: Context):
        await ctx.message.delete()
        ids = self.bot.db.records('SELECT * FROM users')
        matches = re.findall(r"<@(\d+?)>", ctx.message.content, re.MULTILINE)
        for id in matches:
            if id not in ids:
                self.bot.db.add_user(id, True)
            else:
                self.bot.db.execute('UPDATE users SET whitelisted = ? WHERE id = ?', True, id)

        embed: Embed = Embed(title='Whitelist', description=f'Successfully whitelisted {len(matches)} users',
                             colour=0x00ff00)
        self.bot.webhook.send('client', embed)

    @command(name='whitelistfriends')
    async def whitelist_friends(self, ctx: Context):
        await ctx.message.delete()
        user: ClientUser = self.bot.user
        ids = self.bot.db.records('SELECT * FROM users')
        for friend in user.friends:
            if friend.id not in ids:
                self.bot.db.add_user(friend.id, True)
            else:
                self.bot.db.execute('UPDATE users SET whitelisted = ? WHERE id = ?', True, friend.id)

        embed: Embed = Embed(title='Whitelist', description=f'Successfully whitelisted {len(user.friends)} friends',
                             colour=0x00ff00)
        self.bot.webhook.send('client', embed)

    @command(name='-whitelist')
    async def remove_whitelist(self, ctx: Context):
        await ctx.message.delete()
        ids = self.bot.db.records('SELECT * FROM users')
        matches = re.findall(r"<@(\d+?)>", ctx.message.content, re.MULTILINE)
        for id in matches:
            if id not in ids:
                self.bot.db.add_user(id)
            else:
                self.bot.db.execute('UPDATE users SET whitelisted = ? WHERE id = ?', False, id)

        embed: Embed = Embed(title='Whitelist', description=f'Successfully removed whitelist from {len(matches)} users',
                             colour=0x00ff00)
        self.bot.webhook.send('client', embed)


def setup(bot):
    bot.add_cog(Users(bot))
