from discord.ext import commands
import discord
from discord import ApplicationContext, slash_command
from datetime import datetime

class Utility(commands.Cog):

    def __init__(self, client):

        self.client = client
        

    @slash_command(name = "ping")
    async def ping(self, ctx : ApplicationContext):

        embed = discord.Embed(title = "Ping", color = ctx.author.color, timestamp = datetime.now())

        embed.add_field(name = "Latency:", value = f"{round(self.client.latency * 1000)}ms")

        await ctx.respond(embed = embed)


    @slash_command(name = "help")
    async def help(self, ctx : ApplicationContext):

        embed = discord.Embed(title = "Help", color = ctx.author.color, timestamp= datetime.now())

        embed.add_field(name = "</balance:1037791753496969316>:", value = "Lets you check the amount of money you have to bet", inline = False)
        embed.add_field(name = "</bet:1042886759555547146>:", value = "Lets you bet on the teams that are playing on the current day", inline = False)
        embed.add_field(name = "</ping:1043105717189615657>:", value = "Returns the latency of the bot", inline = False)

        await ctx.respond(embed = embed)


def setup(client):
    client.add_cog(Utility(client))
