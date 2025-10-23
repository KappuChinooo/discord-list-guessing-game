from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord
from game.game import GameSession
from game.state import ChannelStateManager
from discord_bot.ui.embeds import make_game_embed
from discord_bot.ui.start_game_view import StartGameView
import random

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
        if self.state_manager.get_game(channel_id=channel_id):
            await interaction.response.send_message("Game already active.", ephemeral=True)
            return
        game = await self.state_manager.start_game(channel_id, mode, favourites_number, hated_number)
        embed = await make_game_embed([])
        view = StartGameView(interaction.user.id, game)
        msg = await interaction.response.send_message(embed=embed, view=view)
        view.message = msg


    @nextcord.slash_command(name="end", description="Ends the ongoing game")
    async def end_game(self, interaction: Interaction):
        channel_id = interaction.channel.id
        if self.state_manager.get_game(channel_id) is None:
            await interaction.response.send_message("There is no active game in this channel.", ephemeral=True)
            return
        await self.state_manager.end_game(channel_id)
        await interaction.response.send_message("Game ended.")


    @nextcord.slash_command(name="generate_list", description="testing")
    async def gen_list(self, interaction: Interaction):
        channel_id = interaction.channel.id
        if self.state_manager.get_game(channel_id=channel_id) is None:
            await interaction.response.send_message("no game", ephemeral=True)
            return
        game: GameSession = self.state_manager.get_game(channel_id)
        for player in range(4):
            for _ in range(3):
                await game.submit_entry(player, str(random.randint(0, 20)), True)
                await game.submit_entry(player, str(random.randint(0, 20)), False)
        await interaction.response.send_message("done", ephemeral=True)


