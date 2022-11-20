import sys

sys.path.append(sys.path[0].replace("\\views", ''))

from discord.ui import Modal, InputText
from discord import InputTextStyle
import discord
from dbFunctions import updateBalance, updateBet, lowFunds, bonusUpdate


class BetModal(Modal):
    def __init__(self, *args, teamBettedOn, matchID, view, **kwargs):
        super().__init__(*args, **kwargs)

        self.view = view

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

                bonusAmount = bonusUpdate(userID = interaction.user.id)

                homeTeamButton = self.view.get_item("homeTeamBtn")
                awayTeamButton = self.view.get_item("awayTeamBtn")

                homeTeamButton.disabled = True
                awayTeamButton.disabled = True

                await interaction.response.edit_message(view = self.view)
                await interaction.followup.send(f"You betted {value} for {self.teamBettedOn}\nYou have also received an additional bonus of {bonusAmount}", ephemeral = True)


            except lowFunds:
                await interaction.response.send_message(f"You dont have enough money to bet {value}", ephemeral = True)
      

        except ValueError:
           await interaction.response.send_message(content = "Amount Entered Must Be A Number", ephemeral = True)