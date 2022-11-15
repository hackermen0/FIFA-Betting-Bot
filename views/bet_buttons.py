from views.bet_modal import BetModal
from discord.ui import Button
import discord



class homeTeamButton(Button):
    def __init__(self, label : str, disabled : bool, matchID : str):

        super().__init__(style = discord.ButtonStyle.green, label = label, disabled = disabled, custom_id = 'homeTeamBtn', row = 1)

        self.label = label
        self.matchID = matchID

    async def callback(self, interaction):

        modal = BetModal(title = f"Betting for {self.label}", teamBettedOn = self.label, matchID = self.matchID, view = self.view)

        await interaction.response.send_modal(modal)
        await interaction.edit_original_response(view = self.view)

        
    

class awayTeamButton(Button):
    def __init__(self, label : str, disabled : bool, matchID: str):

        super().__init__(style = discord.ButtonStyle.green, label = label, disabled = disabled, custom_id = 'awayTeamBtn', row = 1)

        self.label = label
        self.matchID = matchID

    async def callback(self, interaction):

        modal = BetModal(title = f"Betting for {self.label}", teamBettedOn = self.label, matchID = self.matchID, view = self.view)

        await interaction.response.send_modal(modal)
        await interaction.edit_original_response(view = self.view)