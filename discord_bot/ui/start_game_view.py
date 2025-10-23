from nextcord import ui, Interaction, Embed, ButtonStyle
from game.game import GameSession
from discord_bot.ui.list_entry import ListMenu
from discord_bot.ui.embeds import make_list_embed, make_entry_embed
from discord_bot.ui.guessing import GuessingView

class StartGameView(ui.View):
    def __init__(self, host_id: int, game: GameSession):
        super().__init__(timeout=None)
        self.host_id = host_id
        self.game = game
        self.message = None

    @ui.button(label="Start Game", style=ButtonStyle.grey)
    async def start(self, button, interaction: Interaction):
        if self.game is None:
            return
        if interaction.user.id != self.host_id:
            await interaction.response.send_message("Only host can start game.", ephemeral=True)
            return

        if not self.game.list_owners:
            await interaction.response.send_message("No one has submitted their list yet.", ephemeral=True)
            return
        
        await interaction.response.defer()

        await interaction.message.edit(view=None)

        entry = await self.game.next_entry()
        if entry:
            print("game started")
            embed = make_entry_embed(self.game.mode, entry.name)
            await interaction.channel.send(embed=embed, view=GuessingView(self.game, entry))

    
    @ui.button(label="Create List", style=ButtonStyle.blurple)
    async def create_list(self, button: ui.Button, interaction: Interaction):
        menu = ListMenu(user_id=interaction.user.id, game=self.game)
        embed = make_list_embed([], [])
        await interaction.response.send_message(embed=embed, view=menu, ephemeral=True)
        menu.list_message = await interaction.original_message()
        menu.game_message = self.message


