import asyncio
import glob
import sys
import threading
from datetime import datetime
from http.client import HTTPException
from threading import Timer
from asyncio import sleep

import tzlocal
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import discord
from discord.embeds import Embed
from discord.errors import LoginFailure
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, \
    MissingPermissions, BotMissingPermissions
from discord.ext.commands.context import Context
from discord.message import Message

from lib.config import Config
from lib.scraped_user import ScrapedUser
from discord.permissions import Permissions
from lib.webhook import WebhookHandler
from lib.utils import Utils
from lib.db import DB
from lib.apihelper import ApiHelper
from lib.api import app

COGS = [path.split("\\")[-1][:-3] if "\\" in path else path.split("/")[-1][:-3] for path in
        glob.glob('./lib/cogs/*.py')]
COMMAND_ERROR_REGEX = r"Command raised an exception: (.*?(?=: )): (.*)"
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument, RuntimeError)


class Ready(object):
    def __init__(self) -> None:
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog) -> None:
        setattr(self, cog, True)
        print(f" - {cog} cog ready")

    def all_ready(self) -> bool:
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.TOKEN = None
        self.VERSION = None
        self.ready: bool = False
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
        self.cogs_ready: Ready = Ready()
        self.config: Config = Config()
        self.db: DB = DB()
        self.db.build()
        self.api_helper: ApiHelper = ApiHelper(self.config.token, self.config.password)
        self.utils: Utils = Utils(self)
        self.invis = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
        self.recieved = 0
        self.sent = 0
        self.webhook: WebhookHandler = WebhookHandler(self.config.user, self.config.client, self.config.guild,
                                                      self.config.error)
        super().__init__(
            command_prefix=self.config.prefix,
            self_bot=True,
            status=discord.Status.invisible
        )

        self.scheduler.add_job(self.check_update, trigger='cron', minute='0,30')

    def check_update(self) -> None:
        if self.utils.behind():
            embed: Embed = Embed(title='New update available!',
                                 description='Run the command `>update` to update the self bot', colour=0xff0000)
            self.webhook.send('error', embed)

    def setup(self) -> None:
        for cog in COGS:
            super().load_extension(f"lib.cogs.{cog}")
            self.cogs_ready.ready_up(cog)
        print("All Cogs Ready")

    async def mfa(self):
        return await self.api_helper.mfa_enabled()

    def run(self, version) -> None:

        self.VERSION = version

        print("Registering Cogs...")
        self.setup()

        self.TOKEN = self.config.token
        print("Signing into account...")
        try:
            super().run(self.TOKEN, reconnect=True)
        except LoginFailure:
            embed: Embed = Embed(title="Error logging in",
                                 description="Replace old discord token with new token then start bot again!",
                                 colour=0xff0000)
            self.webhook.send('client', embed=embed)
            sys.exit()

    async def process_commands(self, message) -> None:
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

    async def on_connect(self) -> None:
        if not self.ready:
            self.scheduler.start()
            embed = discord.Embed(title="Now Online!", description="SelfBot is now online!", colour=0xff00ff,
                                  timestamp=datetime.utcnow())
            fields = [
                ("Creator:", "`gccody#0001`", True),
                ("Description:", "`This is a SelfBot created for fun`", True)
            ]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name=f"{self.user.display_name}#{self.user.discriminator}")
            embed.set_footer(text="Gccody#0001 |")
            while not self.cogs_ready.all_ready():
                print([getattr(self.cogs_ready, cog) for cog in COGS])
                await sleep(0.5)

            print(f"Bot Ready, Logged in as {bot.user.display_name}#{bot.user.discriminator}!")
            Timer(2, self.ready_up, ()).start()
            self.webhook.send('client', embed)
            # t = threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": "127.0.0.1", "port": 8000})
            # t.start()
        else:
            print("Bot Reconnected")

    async def on_ready(self, *args, **kwargs):
        for guild in self.guilds:
            payload = {
                "op": 14,
                "d": {
                    "guild_id": str(guild.id),
                    "typing": True,
                    "threads": False,
                    "activities": True,
                    "members": [],
                    "channels": {
                        str(guild.channels[0].id): [
                            [
                                0,
                                99
                            ]
                        ]
                    }
                }
            }

            asyncio.ensure_future(self.ws.send_as_json(payload), loop=self.loop)

    def ready_up(self) -> None:
        self.ready = True

    async def on_disconnect(self):
        print(f"Bot Disconnected, Retrying to sign into user {self.user.display_name}#{self.user.discriminator}")

    async def on_error(self, err, *args, **kwargs) -> None:
        if 'command_error' in err:
            return
        vals = str(args[1]).split(":")
        embed: Embed = Embed(title=vals[1], description=f"```{':'.join(vals[2:]).strip()}```", colour=0xff0000)
        print(err, args)
        self.webhook.send('error', embed)
        # raise

    async def on_command_error(self, ctx: Context, exc) -> None:
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")
        elif isinstance(exc, CommandOnCooldown):
            await ctx.message.delete()
            embed: Embed = Embed(title='Command on Cooldown', description=f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} seconds.", colour=0xff0000)
            self.webhook.send('error', embed)
        elif isinstance(exc, MissingPermissions):
            pass
        elif isinstance(exc, BotMissingPermissions):
            await ctx.message.delete()
            embed: Embed = Embed(title='Permissions Error', description=f">>> {exc}", colour=0xff0000)
            self.webhook.send('error', embed)
        elif isinstance(exc, HTTPException):
            embed: Embed = Embed(title="Http Error", description='Message failed to send', colour=0xff0000)
            self.webhook.send('error', embed)
        elif hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                embed: Embed = Embed(title="Http Error", description='Message failed to send', colour=0xff0000)
                self.webhook.send('error', embed)
            if isinstance(exc.original, discord.Forbidden):
                await ctx.message.delete()
                embed: Embed = Embed(title='Forbidden Error', description='Insufficient Permissions', colour=0xff0000)
                self.webhook.send('error', embed)
            else:
                raise exc.original

        else:
            raise exc

    async def on_message(self, message: Message) -> None:
        if message.author.id == 507214515641778187:
            await self.process_commands(message)
            self.sent += 1
        else:
            self.recieved += 1
            if self.config.auto_scrape:
                self.db.add_user(str(message.author.id))


bot: Bot = Bot()
