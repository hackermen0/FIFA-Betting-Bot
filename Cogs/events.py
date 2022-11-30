from discord.ext import commands, tasks
from itertools import cycle
import discord


status = cycle(["Use /help", "Who Will Win Today"])

class Events(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mention in message.content:
            await message.channel.send("Use the </help:1043887595882561658> for additional information")


    @tasks.loop(seconds = 15)
    async def change_status(self):
        await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = next(status)))


def setup(client):
    client.add_cog(Events(client))

