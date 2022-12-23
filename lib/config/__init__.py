import json
import re


class Config():
    valid_keys = ['threads', 'token', 'user', 'client', 'guild', 'error', 'guildId']
    TOKEN_REGEX = r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}'
    WEBHOOK_REGEX = r'https://discord.com\/api\/webhooks\/([^\/]+)\/([^\/]+)'

    def __init__(self) -> None:
        with open('config.json', 'r', encoding='utf-8') as f:
            self.__data = json.loads(f.read())
        self.threads: int = self.__data["threads"]
        self.token: str = self.__data["token"]
        self.scrape_delay: int = self.__data["scrape_delay"]
        self.default_language: str = self.__data["default_language"]
        self.user: str = self.__data["user"]
        self.client: str = self.__data["client"]
        self.guild: str = self.__data["guild"]
        self.error: str = self.__data["error"]
        self.guildId: str = self.__data["guildId"]

    def __save_config(self) -> None:
        with open('config.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.__data, sort_keys=False, indent=2))

    def set(self, key: str, value: any) -> None:
        if not self.__valid_key(key): raise KeyError(f"Invalid Key only valid keys are {self.valid_keys.__str__()}")
        self.__validate(key, value)
        exec(f"self.{key} = value")
        self.__data[key] = value
        self.__save_config()

    def __valid_key(self, key: str):
        return key in self.valid_keys

    def __validate(self, key: str, value: any) -> None:
        match key:
            case 'threads':
                if int(value) <= 0: raise ValueError("Thread count can't be less then or equal to 0")
            case 'token':
                if not re.match(self.TOKEN_REGEX, str(value)): raise Exception("Invalid Discord Token")
            case 'guildId':
                return
            case _:
                if not re.match(self.WEBHOOK_REGEX, str(value)): raise Exception("Invalid Discord Webhook Url")
