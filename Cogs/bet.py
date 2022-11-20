import sys

sys.path.append(sys.path[0].replace("\\Cogs", ''))

from discord.ui import View
from discord.ext import commands, pages
from discord import ApplicationContext, slash_command
from views.navigation_buttons import forwardButton, backwardButton, firstButton, lastButton, PageIndicator
from views.bet_buttons import homeTeamButton, awayTeamButton
from views.donation_button import donationButton
from dbFunctions import checkBetExists, checkUserExists
import discord
from datetime import datetime

from MatchData import Match


class Bet(commands.Cog):
    def __init__(self, client):
        self.disabledValue = False
        self.client = client
        self.pages = []
        self.guildID = 506485291914100737
        self.channelID = 894851964406468669
        

    @slash_command(name = 'bet', description = "Lets you bet on the teams that are playing on the current day")
    async def bet(self, ctx : ApplicationContext):

        if checkUserExists(ctx.user.id) == True:
                        
            matchObject = Match()

            data = matchObject.getData()

            dateToday = data[0]['fixture']['date']
            
            embedList = []

            matchBannerList = []

            buttonList = []

            guild = await self.client.fetch_guild(self.guildID)

            channel = await guild.fetch_channel(self.channelID)

            matchBannerMessage = await channel.history(limit = 1).flatten()


            if matchBannerMessage[0].content != str(dateToday):

                await ctx.respond("Loading...", ephemeral = True)

                for pos, match in enumerate(data):

                    matchObject.createBanner(pos)

                    matchBanner = discord.File(f"./static/images/matchBanner{pos}.png", filename=f"matchBanner{pos}.png")

                    matchBannerList.append(matchBanner)

                matchBannerMessage = await channel.send(content = str(dateToday), files = matchBannerList)

                await ctx.edit(content = "Finished Loading!!!")  


            for pos, match in enumerate(data):  

                matchID = match['fixture']['id']
                matchTitle = match["league"]['name']
                thumbnail = match['league']['logo']
                venueCity = match['fixture']['venue']['city']
                stadium = match['fixture']['venue']['name']
                matchVenueDisplay = f"{stadium}, {venueCity}"
                matchStatusDisplay = match['fixture']['status']['long']
                matchStatusCode = match['fixture']['status']['short']
                matchDate = match['fixture']['date'][:-15]
                matchTime = match['fixture']['date'][:-9][11:]
                homeTeamName = match['teams']['home']['name']
                awayTeamName = match['teams']['away']['name']

                embed = discord.Embed(title = matchTitle, color = ctx.author.color, timestamp = datetime.now())
                embed.set_author(name = 'FIFA Betting Bot', icon_url = "https://cdn.discordapp.com/attachments/894851964406468669/1043592586151071925/botpfp.png")
                embed.set_footer(text = f"Used by {ctx.author}")
                embed.set_thumbnail(url = thumbnail)
                embed.add_field(name = 'Status:', value = matchStatusDisplay, inline = False)
                embed.add_field(name = "Status Code", value = matchStatusCode)
                embed.add_field(name = 'Venue:', value = matchVenueDisplay, inline = False)
                embed.add_field(name = 'Date:', value = matchDate, inline = True)
                embed.add_field(name = 'Time:', value = matchTime, inline = True)

                if type(matchBannerMessage) == list:
                    embed.set_image(url = matchBannerMessage[0].attachments[pos].url)

                else:
                    embed.set_image(url = matchBannerMessage.attachments[pos].url)


                embedList.append((embed))


                if checkBetExists(matchID, ctx.author.id) == True or matchStatusCode != 'NS':
                    self.disabledValue = True  
                else: 
                    self.disabledValue = False


                homeTeamButtonObject = homeTeamButton(label = homeTeamName, disabled = self.disabledValue, matchID = matchID) 
                awayTeamButtonObject = awayTeamButton(label = awayTeamName, disabled = self.disabledValue, matchID = matchID)
                donationButtonObject = donationButton()
            
                buttonList.append((homeTeamButtonObject, awayTeamButtonObject))

            

            
            homeTeamButtonObject, awayTeamButtonObject = buttonList[0]
            
            view = View(homeTeamButtonObject, awayTeamButtonObject, donationButtonObject)
            paginator = pages.Paginator(embedList, custom_view = view)

            paginator.embedList = embedList     
            paginator.buttonList = buttonList


            paginator.add_button(forwardButton())
            paginator.add_button(backwardButton())
            paginator.add_button(firstButton())
            paginator.add_button(lastButton())
            paginator.add_button(PageIndicator(label = f"1/{len(embedList)}"))

            await paginator.respond(ctx.interaction)

        else:
            await ctx.respond("You don't seem to have a balance\nUse the /balance command to create a balance", ephemeral = True)
            
            
def setup(client):
    client.add_cog(Bet(client))
