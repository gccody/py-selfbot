import datetime
import urllib.parse

import requests


class ApiHelper:
    BASE = "https://discord.com/api/v9/"

    def __init__(self, token: str, password: str):
        self.password = password
        self.token = token
        self.headers = {'Authorization': f"{self.token}", 'Content-Type': 'application/json'}

    def timeout_user(self, user_id: str, guild_id: str, minutes: int, reason: str):
        endpoint = f'guilds/{guild_id}/members/{user_id}'
        url = self.BASE + endpoint
        timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)).isoformat()
        json = {'communication_disabled_until': timeout, 'x-audit-log-reason': urllib.parse.quote(reason)}
        session = requests.patch(url, json=json, headers=self.headers)
        return session.status_code in range(200, 299), session.json()

    def remove_timeout(self, user_id: str, guild_id: str):
        endpoint = f'guilds/{guild_id}/members/{user_id}'
        url = self.BASE + endpoint
        json = {'communication_disabled_until': None}
        session = requests.patch(url, json=json, headers=self.headers)
        return session.status_code in range(200,299), session.json()

    def edit_me(self, data):
        url = "https://discord.com/api/v9/users/@me"
        session = requests.patch(url, json=data, headers=self.headers)
        return session.status_code in range(200, 299), session.json()

    def change_password(self, new: str, code: str | None):
        data = {'password': self.password, 'new_password': new}
        if code: data['code'] = code
        res, data = self.edit_me(data)
        if res: self.password = new
        return res, data

    def change_email(self, email: str, code: str | None):
        data = {'email': email, "password": self.password}
        if code: data['code'] = code
        return self.edit_me(data)

    def set_username(self, username: str, discrim: str):
        if len(discrim) != 4: raise ValueError("Discriminator must be a length of 4")
        data = {'discriminator': discrim, 'password': self.password, 'username': username}
        return self.edit_me(data)

    def remove_guild(self, guild_id: str, code: str | None):
        url =  f"https://discord.com/api/v9/guilds/{guild_id}/delete"
        data = {}
        if code: data['code'] = code
        session = requests.post(url, json=data, headers=self.headers)
        return session.status_code in range(200, 299), session.json()

    def get_channels(self, guild_id: str):
        url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
        session = requests.get(url, headers=self.headers)
        return [channel['id'] for channel in session.json()]

    def mfa_enabled(self):
        url = "https://discord.com/api/v9/users/@me"
        session = requests.get(url, headers=self.headers)
        return session.json()['mfa_enabled']
