import datetime
import requests


class ApiHelper:
    BASE = "https://discord.com/api/v9/"

    def __init__(self, token: str):
        self.token = token

    def timeout_user(self, user_id: str, guild_id: str, minutes: int):
        endpoint = f'guilds/{guild_id}/members/{user_id}'
        headers = {"Authorization": f"Bearer {self.token}"}
        url = self.BASE + endpoint
        timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)).isoformat()
        json = {'communication_disabled_until': timeout}
        session = requests.patch(url, json=json, headers=headers)
        return session.status_code in range(200, 299)