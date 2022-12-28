import json
import re


class Config():
    valid_keys = ['threads', 'token', 'scrape_delay', 'default_language', 'email', 'password', 'user', 'client', 'guild', 'error', 'guildId']
    TOKEN_REGEX = r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}'
    WEBHOOK_REGEX = r'https://discord.com\/api\/webhooks\/([^\/]+)\/([^\/]+)'

    def __init__(self) -> None:
        with open('config.json', 'r', encoding='utf-8') as f:
            self.__data = json.loads(f.read())
        self.threads: int = self.__data["threads"] if 'threads' in self.__data else 0
        self.token: str = self.__data["token"] if 'token' in self.__data else ""
        self.scrape_delay: int = self.__data["scrape_delay"] if 'scrape_delay' in self.__data else 0
        self.default_language: str = self.__data["default_language"] if 'default_language' in self.__data else ""
        self.email = self.__data["email"] if 'email' in self.__data else ""
        self.password: str = self.__data["password"] if 'password' in self.__data else ""
        self.user: str = self.__data["user"] if 'user' in self.__data else ""
        self.client: str = self.__data["client"] if 'client' in self.__data else ""
        self.guild: str = self.__data["guild"] if 'guild' in self.__data else ""
        self.error: str = self.__data["error"] if 'error' in self.__data else ""
        self.guildId: str = self.__data["guildId"] if 'guildId' in self.__data else ""

    def __save_config(self) -> None:
        with open('config.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.to_json(), sort_keys=False, indent=2))

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
            case 'user', 'client', 'guild', 'error':
                if not re.match(self.WEBHOOK_REGEX, str(value)): raise Exception("Invalid Discord Webhook Url")
            case _:
                return

    def to_json(self):
        return {
            "threads": self.threads,
            "token": self.token,
            "scrape_delay": self.scrape_delay,
            "default_language": self.default_language,
            "email": self.email,
            "password": self.password,
            "": "Do Not Touch Below! If No Webhooks Then Run '.setup' Command",
            "guildId": self.guildId,
            "user": self.user,
            "client": self.client,
            "guild": self.guild,
            "error": self.error
        }