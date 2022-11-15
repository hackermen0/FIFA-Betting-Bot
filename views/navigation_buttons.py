import discord
from discord.ext.pages import PaginatorButton


# def updatingButtonStatus(ctx, homeTeamButton, awayTeamButton, matchID, matchStatusCode):
#     if checkBetExists(matchID, ctx.author.id) == True or matchStatusCode != 'NS':
#             homeTeamButton.disabled = True
#             awayTeamButton.disabled = True


class forwardButton(PaginatorButton):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.green, label = ' >', disabled = False, custom_id = 'forwardBtn', button_type = "next", row = 0)


    async def callback(self, interaction: discord.Interaction):

        pageCount = self.paginator.current_page
        maxPage = self.paginator.page_count
        embedList = self.paginator.embedList  
        buttonList = self.paginator.buttonList

        forwardbutton = self.paginator.get_item('forwardBtn')
        lastButton = self.paginator.get_item('lastBtn')

        backButton = self.paginator.get_item('backwardBtn')
        firstButton = self.paginator.get_item('firstBtn')

    
        if int(pageCount) == int(maxPage - 1):
  
            lastButton.disabled = True
            forwardbutton.disabled = True


        backButton.disabled = False
        firstButton.disabled = False


        pageIndicatorButton = self.paginator.get_item("page")

        pageIndicatorButton.label = f"{pageCount + 2}/{maxPage + 1}"

        self.paginator.current_page += 1

        homeTeamButtom, awayTeamButton = buttonList[self.paginator.current_page]
        embed = embedList[self.paginator.current_page]

        prevHomeTeamButton = self.paginator.get_item("homeTeamBtn")
        prevAwayTeamButton = self.paginator.get_item("awayTeamBtn")

        self.paginator.remove_item(prevHomeTeamButton)
        self.paginator.remove_item(prevAwayTeamButton)

        self.paginator.add_item(homeTeamButtom)
        self.paginator.add_item(awayTeamButton)

        
        await interaction.response.edit_message(view = self.paginator, embed = embed)





class backwardButton(PaginatorButton):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.green, label = ' <', disabled = True, custom_id = 'backwardBtn', button_type = "prev", row = 0)
      

    async def callback(self, interaction: discord.Interaction):

        pageCount = self.paginator.current_page
        maxPage = self.paginator.page_count
        embedList = self.paginator.embedList  
        buttonList = self.paginator.buttonList

        forwardbutton = self.paginator.get_item('forwardBtn')
        lastButton = self.paginator.get_item('lastBtn')

        backButton = self.paginator.get_item('backwardBtn')
        firstButton = self.paginator.get_item('firstBtn')

        if int(pageCount) == 1:
  
            backButton.disabled = True
            firstButton.disabled = True

        forwardbutton.disabled = False
        lastButton.disabled = False

        
        pageIndicatorButton = self.paginator.get_item("page")

        pageIndicatorButton.label = f"{pageCount}/{maxPage + 1}"


        self.paginator.current_page -= 1

        homeTeamButtom, awayTeamButton = buttonList[self.paginator.current_page]
        embed = embedList[self.paginator.current_page]

        prevHomeTeamButton = self.paginator.get_item("homeTeamBtn")
        prevAwayTeamButton = self.paginator.get_item("awayTeamBtn")

        self.paginator.remove_item(prevHomeTeamButton)
        self.paginator.remove_item(prevAwayTeamButton)

        self.paginator.add_item(homeTeamButtom)
        self.paginator.add_item(awayTeamButton)

        
        await interaction.response.edit_message(view = self.paginator, embed = embed)

        
class lastButton(PaginatorButton):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.green, label = ' >>', disabled = False, custom_id = 'lastBtn', button_type = "last", row = 0)


    async def callback(self, interaction: discord.Interaction):

        pageCount = self.paginator.current_page
        maxPage = self.paginator.page_count
        embedList = self.paginator.embedList  
        buttonList = self.paginator.buttonList

        forwardbutton = self.paginator.get_item('forwardBtn')
        lastButton = self.paginator.get_item('lastBtn')

        backButton = self.paginator.get_item('backwardBtn')
        firstButton = self.paginator.get_item('firstBtn')

        forwardbutton.disabled = True
        lastButton.disabled = True

        backButton.disabled = False
        firstButton.disabled = False

        pageIndicatorButton = self.paginator.get_item("page")

        pageIndicatorButton.label = f"{maxPage + 1}/{maxPage + 1}"
 

        self.paginator.current_page = int(maxPage)

        homeTeamButtom, awayTeamButton = buttonList[self.paginator.current_page]
        embed = embedList[self.paginator.current_page]

        prevHomeTeamButton = self.paginator.get_item("homeTeamBtn")
        prevAwayTeamButton = self.paginator.get_item("awayTeamBtn")

        self.paginator.remove_item(prevHomeTeamButton)
        self.paginator.remove_item(prevAwayTeamButton)

        self.paginator.add_item(homeTeamButtom)
        self.paginator.add_item(awayTeamButton)

        
        await interaction.response.edit_message(view = self.paginator, embed = embed)


class firstButton(PaginatorButton):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.green, label = ' <<', disabled = True, custom_id = 'firstBtn', button_type = "first", row = 0)

    async def callback(self, interaction: discord.Interaction):

        maxPage = self.paginator.page_count
        embedList = self.paginator.embedList  
        buttonList = self.paginator.buttonList

        forwardbutton = self.paginator.get_item('forwardBtn')
        lastButton = self.paginator.get_item('lastBtn')

        backButton = self.paginator.get_item('backwardBtn')
        firstButton = self.paginator.get_item('firstBtn')

        forwardbutton.disabled = False
        lastButton.disabled = False

        backButton.disabled = True
        firstButton.disabled = True

        pageIndicatorButton = self.paginator.get_item("page")

        pageIndicatorButton.label = f"1/{maxPage + 1}"

        self.paginator.current_page = 0

        homeTeamButtom, awayTeamButton = buttonList[self.paginator.current_page]
        embed = embedList[self.paginator.current_page]

        prevHomeTeamButton = self.paginator.get_item("homeTeamBtn")
        prevAwayTeamButton = self.paginator.get_item("awayTeamBtn")

        self.paginator.remove_item(prevHomeTeamButton)
        self.paginator.remove_item(prevAwayTeamButton)

        self.paginator.add_item(homeTeamButtom)
        self.paginator.add_item(awayTeamButton)

        
        await interaction.response.edit_message(view = self.paginator, embed = embed)

class PageIndicator(PaginatorButton):
    def __init__(self, label):

        super().__init__(button_type = "page_indicator", style = discord.ButtonStyle.gray, label = label, disabled = True, custom_id = "page")