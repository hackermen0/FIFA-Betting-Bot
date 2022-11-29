from discord.ui import Select
from discord import SelectOption
import discord

globalLeaderboard = SelectOption(label = "Global", emoji = "🌐", value = 'global', default = False)
localLeaderboard = SelectOption(label = "Server", emoji = "🏠", value = 'local', default = False)

class LeaderboardSelect(Select):
    def __init__(self, embeds : tuple):

        self.embeds = embeds

        super().__init__(custom_id = "lb-select", options = [localLeaderboard, globalLeaderboard], disabled = False, max_values = 1, min_values = 1, row = 0, placeholder = "Choose your leaderboard type")



    async def callback(self, interaction: discord.Interaction):
        

        if self.values[0] == "local":

            embed = self.embeds[0]

            await interaction.response.edit_message(embed = embed)

        if self.values[0] == "global":

            embed = self.embeds[1]

            await interaction.response.edit_message(embed = embed)