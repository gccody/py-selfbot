from datetime import datetime

from discord import Webhook, RequestsWebhookAdapter, Embed, NotFound

valid_keys: list[str] = ['user', 'client', 'guild', 'error']


class WebhookHandler:
    def __init__(self, user: str, client: str, guild: str, error: str) -> None:
        self.user = Webhook.from_url(user, adapter=RequestsWebhookAdapter())
        self.client = Webhook.from_url(client, adapter=RequestsWebhookAdapter())
        self.guild = Webhook.from_url(guild, adapter=RequestsWebhookAdapter())
        self.error = Webhook.from_url(error, adapter=RequestsWebhookAdapter())
        self.logo_path = "https://i.imgur.com/n5mioQi.jpg"

    def set(self, key: str, url: str) -> None:
        if not self.__valid_key(key): raise KeyError(f"Invalid Key only valid keys are {valid_keys.__str__()}")
        exec(f"self.{key} = Webhook.from_url(url, adapter=RequestsWebhookAdapter())")

    def send(self, key: str, embed: Embed) -> None:
        if not self.__valid_key(key): raise KeyError(f"Invalid Key only valid keys are {valid_keys.__str__()}")
        embed.set_footer(text="Made By Gccody", icon_url=self.logo_path)
        embed.set_thumbnail(url=self.logo_path)
        embed.timestamp = datetime.utcnow()
        try:
            exec(f"self.{key}.send(username=\"{key.title()} Update\", embed=embed)")
        except NotFound:
            print("USE >setup TO GET WEBHOOKS WORKING PROPERLY!!!!!!!!")
            print("USE >setup TO GET WEBHOOKS WORKING PROPERLY!!!!!!!!")
            print("USE >setup TO GET WEBHOOKS WORKING PROPERLY!!!!!!!!")
            print("USE >setup TO GET WEBHOOKS WORKING PROPERLY!!!!!!!!")

    def print_url(self, key) -> str:
        exec(f"print(self.{key})")

    def __valid_key(self, key: str) -> bool:
        return key in valid_keys
