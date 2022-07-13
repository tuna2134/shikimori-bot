import discord


WEBHOOK_NAME = "shikimori-webhook"
async def send_webhook(self, *args, **kwargs):
    webhook = discord.utils.get(await self.webhooks(), name=WEBHOOK_NAME)
    if webhook is None:
        webhook = await self.create_webhook(name=WEBHOOK_NAME)
    await webhook.send(*args, **kwargs)
