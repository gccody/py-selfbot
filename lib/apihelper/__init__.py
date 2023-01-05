import datetime
import urllib.parse

import aiohttp


class ApiHelper:
    BASE = "https://discord.com/api/v9/"

    def __init__(self, token: str, password: str):
        self.password = password
        self.session = aiohttp.ClientSession()
        self.token = token
        self.headers = {'Authorization': f"{self.token}", 'Content-Type': 'application/json'}

    async def timeout_user(self, user_id: str, guild_id: str, minutes: int, reason: str):
        endpoint = f'guilds/{guild_id}/members/{user_id}'
        url = self.BASE + endpoint
        timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)).isoformat()
        json = {'communication_disabled_until': timeout, 'x-audit-log-reason': urllib.parse.quote(reason)}
        session = await self.session.patch(url, json=json, headers=self.headers)
        return session.status in range(200, 299), await session.json()

    async def remove_timeout(self, user_id: str, guild_id: str):
        endpoint = f'guilds/{guild_id}/members/{user_id}'
        url = self.BASE + endpoint
        json = {'communication_disabled_until': None}
        session = await self.session.patch(url, json=json, headers=self.headers)
        return session.status in range(200, 299), await session.json()

    async def edit_me(self, data):
        url = f"{self.BASE}/users/@me"
        session = await self.session.patch(url, json=data, headers=self.headers)
        return session.status in range(200, 299), await session.json()

    async def change_password(self, new: str, code: str | None):
        data = {'password': self.password, 'new_password': new}
        if code: data['code'] = code
        res, data = self.edit_me(data)
        if res: self.password = new
        return res, data

    async def change_email(self, email: str, code: str | None):
        data = {'email': email, "password": self.password}
        if code: data['code'] = code
        return await self.edit_me(data)

    async def set_username(self, username: str, discrim: str):
        if len(discrim) != 4: raise ValueError("Discriminator must be a length of 4")
        data = {'discriminator': discrim, 'password': self.password, 'username': username}
        return await self.edit_me(data)

    async def remove_guild(self, guild_id: str, code: str | None):
        url = f"{self.BASE}/guilds/{guild_id}/delete"
        data = {}
        if code: data['code'] = code
        session = await self.session.post(url, json=data, headers=self.headers)
        return session.status in range(200, 299), await session.json()

    async def get_channels(self, guild_id: str):
        url = f"{self.BASE}/guilds/{guild_id}/channels"
        session = await self.session.get(url, headers=self.headers)
        return [channel['id'] for channel in await session.json()]

    async def mfa_enabled(self):
        url = f"{self.BASE}/users/@me"
        session = await self.session.get(url, headers=self.headers)
        if session.status in range(200, 299):
            return await session.json()['mfa_enabled']
        else:
            return await session.json()

    async def token_info(self, token: str):
        url = f"{self.BASE}/users/@me"
        session = await self.session.get(url, headers={'Authorization': token, 'Content-Type': 'application/json'})
        return await session.json()

    async def guild_members(self, guild_id):
        url = f"{self.BASE}/guilds/{guild_id}/members"
        session = await self.session.get(url, headers=self.headers)
        return await session.json()
