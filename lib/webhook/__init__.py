from datetime import datetime
from discord import Webhook, RequestsWebhookAdapter, Embed

class WebhookHandler():
  def __init__(self, user: str, client: str, guild: str, error: str) -> None:
    self.user = Webhook.from_url(user, adapter=RequestsWebhookAdapter())
    self.client = Webhook.from_url(client, adapter=RequestsWebhookAdapter())
    self.guild = Webhook.from_url(guild, adapter=RequestsWebhookAdapter())
    self.error = Webhook.from_url(error, adapter=RequestsWebhookAdapter())
    self.logo_path = "https://i.imgur.com/n5mioQi.jpg"

  def setUser(self, url: str) -> None:
    self.user = Webhook.from_url(url, adapter=RequestsWebhookAdapter())

  def setClient(self, url: str) -> None:
    self.client = Webhook.from_url(url, adapter=RequestsWebhookAdapter())

  def setGuild(self, url: str) -> None:
    self.guild = Webhook.from_url(url, adapter=RequestsWebhookAdapter())

  def setError(self, url: str) -> None:
    self.error = Webhook.from_url(url, adapter=RequestsWebhookAdapter())

  def sendUserWebhook(self, embed: Embed) -> None:
    embed.set_footer(text="Made By Gccody", icon_url=self.logo_path)
    embed.set_thumbnail(url=self.logo_path)
    embed.timestamp = datetime.utcnow()
    self.user.send(username="User Update", embed=embed)
  
  def sendClientWebhook(self, embed: Embed) -> None:
    embed.set_footer(text="Made By Gccody", icon_url=self.logo_path)
    embed.set_thumbnail(url=self.logo_path)
    embed.timestamp = datetime.utcnow()
    self.client.send(username="Client Update", embed=embed)

  def sendGuildWebhook(self, embed: Embed) -> None:
    embed.set_footer(text="Made By Gccody", icon_url=self.logo_path)
    embed.set_thumbnail(url=self.logo_path)
    embed.timestamp = datetime.utcnow()
    self.guild.send(username="Guild Update", embed=embed)

  def sendErrorWebhook(self, embed: Embed) -> None:
    embed.set_footer(text="Made By Gccody", icon_url=self.logo_path)
    embed.set_thumbnail(url=self.logo_path)
    embed.timestamp = datetime.utcnow()
    self.error.send(username="Error Update", embed=embed)

# webhook: WebhookHandler = WebhookHandler("https://discord.com/api/webhooks/1020167668378120223/CKwDJLUoC62r86EjBuNVU59WcIomOfFLn5unXkeF8-G-ibHkX3mboMBF6U1tm5PH7grh", "https://discord.com/api/webhooks/1020167668378120223/CKwDJLUoC62r86EjBuNVU59WcIomOfFLn5unXkeF8-G-ibHkX3mboMBF6U1tm5PH7grh", "https://discord.com/api/webhooks/1020167668378120223/CKwDJLUoC62r86EjBuNVU59WcIomOfFLn5unXkeF8-G-ibHkX3mboMBF6U1tm5PH7grh", "https://discord.com/api/webhooks/1020167668378120223/CKwDJLUoC62r86EjBuNVU59WcIomOfFLn5unXkeF8-G-ibHkX3mboMBF6U1tm5PH7grh")
# embed: Embed = Embed()
# embed.set_author(name="Gccody")
# embed.description = "Testing Webhooks"
# embed.colour = 0x00ff00
# webhook.user.url = "https://discord.com/api/webhooks/1020184881424236606/OazuF7I8R6BDmCxJmjS3wrk7h8R0oXkwadzYc7KD2OFhcsmSsDvXquCIUNYGmtaTa9bO"
# webhook.sendUserWebhook(embed)

