import sys

path = sys.path[0].replace('\Cogs', '')
sys.path.append(path)

from discord import ApplicationContext, slash_command, option
from discord.ext import commands
import discord
from dbFunctions import getBalance, redeemBet


#creating a check so only my user can execute the commands in this file
def hackerman(ctx):
    return ctx.author.id == 345234588857270283

class Bal(commands.Cog):
    def __init__(self, client):
        self.client = client


    @slash_command(name = "balance")
    @option(name = "member", required = False, type = discord.Member)
    async def balance(self, ctx : ApplicationContext, member : discord.Member):


            if member == None:

                userID = ctx.author.id


                #If user doesn't have a balance this function also creates a balance for them and returns it value
                userBalance = getBalance(userID, str(ctx.author))

                balanceEmbed = discord.Embed(title = f'{ctx.author} Balance', color = ctx.author.color)
                balanceEmbed.add_field(name = 'Balance: ', value = userBalance)
                
                await ctx.respond(embed = balanceEmbed)

            else:

                userID = member.id

                #If user doesn't have a balance this function also creates a balance for them and returns it value


                userBalance = getBalance(userID, str(f"{member.name}#{member.discriminator}"))

                balanceEmbed = discord.Embed(title = f'{member.name}#{member.discriminator} Balance', color = ctx.author.color)
                balanceEmbed.add_field(name = 'Balance: ', value = userBalance)
                
                await ctx.respond(embed = balanceEmbed)
        

    @commands.check(hackerman)
    @commands.command(name = "redeem")
    async def redeem(self, ctx):

        redeemBet()

        await ctx.respond("Bets Redeemed")


def setup(client):
    client.add_cog(Bal(client))
        