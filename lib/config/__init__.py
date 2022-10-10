import json
import re

class Config():
  TOKEN_REGEX = r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}'
  WEBHOOK_REGEX = r'https://discord.com\/api\/webhooks\/([^\/]+)\/([^\/]+)'
  def __init__(self) -> None:
    with open('config.json', 'r', encoding='utf-8') as f:
      self.__data = json.loads(f.read())
    self.threads: int = self.__data["threads"]
    self.token: str = self.__data["token"]
    self.userLogUrl: str = self.__data["userLogsWebhook"]
    self.clientLogUrl: str = self.__data["clientLogsWebhook"]
    self.guildLogUrl: str = self.__data["guildLogsWebhook"]
    self.errorLogUrl: str = self.__data["errorLogsWebhook"]
  
  def __saveConfig(self) -> None:
    with open('config.json', 'w', encoding='utf-8') as f:
      f.write(json.dumps(self.__data, sort_keys=False, indent=2))

  def setThreads(self, threads: int) -> None:
    if threads <= 0: raise ValueError("Thread count can't be less then or equal to 0")
    self.threads = threads
    self.__data["threads"] = threads
    self.__saveConfig()

  def setToken(self, token: str) -> None:
    if not re.match(self.TOKEN_REGEX, token): raise Exception("Invalid Discord Token")
    self.token = token
    self.__data["token"] = token
    self.__saveConfig()

  def setUserWebhookUrl(self, url: str) -> None:
    if not re.match(self.WEBHOOK_REGEX, url): raise Exception("Invalid Discord Webhook Url")
    self.userLogUrl = url
    self.__data["userLogsWebhook"] = url
    self
    self.__saveConfig()

  def setClientWebhookUrl(self, url: str) -> None:
    if not re.match(self.WEBHOOK_REGEX, url): raise Exception("Invalid Discord Webhook Url")
    self.clientLogUrl = url
    self.__data["clientLogsWebhook"] = url
    self.__saveConfig()

  def setGuildWebhookUrl(self, url: str) -> None:
    if not re.match(self.WEBHOOK_REGEX, url): raise Exception("Invalid Discord Webhook Url")
    self.guildLogUrl = url
    self.__data["guildLogsWebhook"] = url
    self.__saveConfig()

  def setErrorWebhookUrl(self, url: str) -> None:
    if not re.match(self.WEBHOOK_REGEX, url): raise Exception("Invalid Discord Webhook Url")
    self.errorLogUrl = url
    self.__data["errorLogsWebhook"] = url
    self.__saveConfig()



config: Config = Config()