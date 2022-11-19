import sys


path = sys.path[0].replace('\Cogs', '')
sys.path.append(path)


from discord import ApplicationContext, slash_command, option
from discord.ext import commands
import discord
from dbFunctions import getBalance, redeemBet, getLeaderboard
from datetime import datetime



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
                balanceEmbed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
                balanceEmbed.set_footer(text = f"Used by {ctx.author}")
                
                await ctx.respond(embed = balanceEmbed)

            else:

                userID = member.id

                #If user doesn't have a balance this function also creates a balance for them and returns it value


                userBalance = getBalance(userID, str(f"{member.name}#{member.discriminator}"))

                balanceEmbed = discord.Embed(title = f'{member.name}#{member.discriminator} Balance', color = ctx.author.color)
                balanceEmbed.add_field(name = 'Balance: ', value = userBalance)
                balanceEmbed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
                balanceEmbed.set_footer(text = f"Used by {ctx.author}")
                
                
                await ctx.respond(embed = balanceEmbed)

    @slash_command(name = 'leaderboard')
    async def leaderboard(self, ctx : ApplicationContext):

        embed = discord.Embed(title = "Leaderboard", color = ctx.author.color, timestamp = datetime.now())      
        embed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
        embed.set_footer(text = f"Used by {ctx.author}")
        
        moneyList = getLeaderboard()

        for pos, item in enumerate(moneyList):

            if pos == 15:
                break

            userID = item[0]
            balance = item[1]

            User = self.client.get_user(userID)

            embed.add_field(name = f"{pos + 1}) {User.name}#{User.discriminator}:" , value = str(balance), inline = False)

        
        await ctx.respond(embed = embed)

            


    @commands.check(hackerman)
    @commands.command(name = "redeem")
    async def redeem(self, ctx):

        redeemBet()

        await ctx.respond("Bets Redeemed")


def setup(client):
    client.add_cog(Bal(client))
        