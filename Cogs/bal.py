import sys


path = sys.path[0].replace('\Cogs', '')
sys.path.append(path)


from discord import ApplicationContext, slash_command, option
from discord.ext import commands, pages
import discord
from dbFunctions import getBalance, redeemBet, getLeaderboard, getStats
from views.leaderboard_select import LeaderboardSelect
from datetime import datetime



#creating a check so only my user can execute the commands in this file
def hackerman(ctx):
    return ctx.author.id == 345234588857270283

class Bal(commands.Cog):
    def __init__(self, client):
        self.client = client


    @slash_command(name = "balance", description = "Lets you check the amount of money you have to bet")
    @option(name = "member", required = False, type = discord.Member, description = "Let's you check the balance of a server member")
    async def balance(self, ctx : ApplicationContext, member : discord.Member):


            if member == None:

                userID = ctx.author.id

                userBalance = getBalance(userID, str(ctx.author))

                balanceEmbed = discord.Embed(title = f'{ctx.author} Balance', color = ctx.author.color, timestamp = datetime.now())
                balanceEmbed.add_field(name = 'Balance: ', value = userBalance)
                balanceEmbed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
                balanceEmbed.set_footer(text = f"Used by {ctx.author}")
                
                await ctx.respond(embed = balanceEmbed)

            else:

                userID = member.id

                userBalance = getBalance(userID, str(f"{member.name}#{member.discriminator}"), autoCreate = False)

                if userBalance == None:
                    userBalance = "User doesn't have a balance"

                balanceEmbed = discord.Embed(title = f'{member.name}#{member.discriminator} Balance', color = ctx.author.color, timestamp = datetime.now())
                balanceEmbed.add_field(name = 'Balance: ', value = userBalance)
                balanceEmbed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
                balanceEmbed.set_footer(text = f"Used by {ctx.author}")
                
                
                await ctx.respond(embed = balanceEmbed)

    @slash_command(name = 'leaderboard', description = "Shows the leaderboard with the top betters")
    async def leaderboard(self, ctx : ApplicationContext):


        guild = self.client.get_guild(506485291914100737)
        loadingEmoji = discord.utils.get(guild.emojis, name = 'loading')
    
        await ctx.respond(f"Loading {loadingEmoji}")

        localEmbed = discord.Embed(title = "Leaderboard", color = ctx.author.color, timestamp = datetime.now())      
        localEmbed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
        localEmbed.set_footer(text = f"Used by {ctx.author}")

        
        globalEmbed = discord.Embed(title = "Leaderboard", color = ctx.author.color, timestamp = datetime.now())      
        globalEmbed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
        globalEmbed.set_footer(text = f"Used by {ctx.author}")

        moneyList = getLeaderboard()

        i = 0

        for item in moneyList:

            userID = item[0]
            balance = item[1]

            User = await self.client.fetch_user(userID)

            
            if User in ctx.guild.members:

                localEmbed.add_field(name = f"{i + 1}) {User.name}#{User.discriminator}:" , value = str(balance), inline = False)

                i += 1


        for pos, item in enumerate(moneyList):

            if pos == 15:
                break

            userID = item[0]
            balance = item[1]

            User = await self.client.fetch_user(userID)

            globalEmbed.add_field(name = f"{pos + 1}) {User.name}#{User.discriminator}:" , value = str(balance), inline = False)




        view = discord.ui.View(LeaderboardSelect(embeds = (localEmbed, globalEmbed)))

        await ctx.edit(embed = localEmbed, view = view, content = " ")


    @slash_command(name = "stats", description = "Shows the amount of money betted on the current day matches")
    async def stats(self, ctx : ApplicationContext):



        matchDataList = getStats()

        embedList = []

        for data in matchDataList:
            if data['numberOfTeams'] == 2:
                
                teams = list(data.keys())
                team1Name = teams[0]
                team2Name = teams[1]

                team1TotalAmount = data[team1Name]['totalAmount']
                team1NumberOfBets = data[team1Name]['numberOfBets']

                team2TotalAmount = data[team2Name]['totalAmount']
                team2NumberOfBets = data[team2Name]['numberOfBets']

                embed = discord.Embed(title = "Stats", color = ctx.author.color, timestamp = datetime.now())      
                embed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
                embed.set_footer(text = f"Used by {ctx.author}")

                embed.add_field(name = f"Amount betted for **{team1Name}**: ", value = team1TotalAmount, inline = True)
                embed.add_field(name = f"Amount betted for **{team2Name}**: ", value = team2TotalAmount, inline = True)
                embed.add_field(name = "\u2800", value = "\u2800", inline = False)
                embed.add_field(name = f"Number of better's for **{team1Name}**: ", value = team1NumberOfBets, inline = True)
                embed.add_field(name = f"Number of better's for **{team2Name}**: ", value = team2NumberOfBets, inline = True)

                embedList.append(embed)

            if data['numberOfTeams'] == 1:

                teams = list(data.keys())
                team1Name = teams[0]

                team1TotalAmount = data[team1Name]['totalAmount']
                team1NumberOfBets = data[team1Name]['numberOfBets']


                embed = discord.Embed(title = "Stats", color = ctx.author.color, timestamp = datetime.now())      
                embed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
                embed.set_footer(text = f"Used by {ctx.author}")

                embed.add_field(name = f"Amount betted for **{team1Name}**: ", value = team1TotalAmount, inline = True)
                embed.add_field(name = "\u2800", value = "\u2800", inline = False)
                embed.add_field(name = f"Number of better's for **{team1Name}**: ", value = team1NumberOfBets, inline = True)

                embedList.append(embed)



        paginator = pages.Paginator(pages = embedList)


        await paginator.respond(ctx.interaction)
                

            


    @commands.check(hackerman)
    @commands.command(name = "redeem")
    async def redeem(self, ctx):

        redeemBet()

        await ctx.respond("Bets Redeemed")


def setup(client):
    client.add_cog(Bal(client))
        