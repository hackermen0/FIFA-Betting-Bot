from discord import ApplicationContext, slash_command
from discord.ext import commands
import discord
from dbFunctions import getBalance

class Bal(commands.Cog):
    def __init__(self, client):
        self.client = client


    @slash_command(name = "balance")
    async def balance(self, ctx : ApplicationContext):

      
            userID = ctx.author.id

            #If user doesn't have a balance this function also creates a balance for them and returns it value
            userBalance = getBalance(userID, str(ctx.author))

            balanceEmbed = discord.Embed(title = f'{ctx.author} Balance', color = ctx.author.color)
            balanceEmbed.add_field(name = 'Balance: ', value = userBalance)
            
            await ctx.respond(embed = balanceEmbed)

        # else: 

        #     userID = str(member.id)
        #     userBalance = getBalance(userID, str(ctx.author))
        #     balanceEmbed = discord.Embed(title = f'{member.name}#{member.discriminator} Balance')
        #     balanceEmbed.add_field(name = 'Balance: ', value = userBalance)




def setup(client):
    client.add_cog(Bal(client))
        