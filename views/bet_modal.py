import sys

sys.path.append(sys.path[0].replace("\\views", ''))

from discord.ui import Modal, InputText
from discord import InputTextStyle
import discord
from dbFunctions import updateBalance, updateBet, lowFunds


class BetModal(Modal):
    def __init__(self, *args, teamBettedOn, matchID, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label = 'Must be a number', placeholder = 'Enter Amount', style = InputTextStyle.singleline))

        self.teamBettedOn = teamBettedOn
        self.matchID = matchID


    async def callback(self, interaction : discord.Interaction):

        inputValue = self.children[0].value

        try:
            value = abs(round(int(inputValue))) 

            try:

                updateBalance(userID = interaction.user.id, method = "sub", amount = value)
                updateBet(matchID = self.matchID, userID = interaction.user.id, team = self.teamBettedOn, amount = value)
                await interaction.response.send_message(f"You betted {value} for {self.teamBettedOn}", ephemeral = True)

            except lowFunds:
                await interaction.response.send_message(f"You dont have enough money to bet {value}", ephemeral = True)
      

        except ValueError:
           await interaction.response.send_message(content = "Amount Entered Must Be A Number", ephemeral = True)