from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord
from game.state import ChannelStateManager


class GameCog(commands.Cog):
    def __init__(self, bot, state_manager: ChannelStateManager):
        self.bot = bot
        self.state_manager = state_manager



    @nextcord.slash_command(name="start", description="Start a new game")
    async def start_game(self,
                         interaction: Interaction,
                         favourites_number: int = 5,
                         hated_number: int = 5,
                         mode: str = SlashOption(
                             name="mode",
                             choices=["general", "anime", "characters"],
                             default="general")):
        channel_id = interaction.channel.id
        if self.state_manager.get_game(channel_id):
            await interaction.response.send_message("Game already active.", ephemeral=True)
            return
        await self.state_manager.start_game(channel_id, mode, favourites_number, hated_number)
        await interaction.response.send_message("Game started. Do /submit_list to enter to lists")



    @nextcord.slash_command(name="end", description="Ends the ongoing game")
    async def end_game(self, interaction: Interaction):
        channel_id = interaction.channel.id
        if self.state_manager.get_game(channel_id) is None:
            await interaction.response.send_message("There is no active game in this channel.", ephemeral=True)
            return
        await self.state_manager.end_game(channel_id)
        await interaction.response.send_message("Game ended.")



    @nextcord.slash_command(name="submit_list", description="Submits your lists for ongoing game")
    async def submit_list(self, interaction: Interaction):
        channel_id = interaction.channel.id
        if self.state_manager.get_game(channel_id) is None:
            await interaction.response.send_message("There is no active game in this channel.", ephemeral=True)
            return
        game = self.state_manager.get_game(channel_id)
        
        pass
