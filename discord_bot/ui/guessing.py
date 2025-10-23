from nextcord import ui, Interaction, SelectOption
from game.game import GameSession
from game.models import Entry

class GuessingView(ui.View):
    def __init__(self, game, entry):
        super().__init__(timeout=None)
        self.game = game
        self.entry = entry
        self.add_item(OwnerGuessDropdown(game, entry))
        self.add_item(CategoryDropdown(game, entry))

class OwnerGuessDropdown(ui.Select):
    def __init__(self, game: GameSession, entry: Entry):
        # Build options from all players who submitted a list
        self.game = game
        self.entry = entry
        options = [
            SelectOption(label=f"<@{player_id}>", value=str(player_id))
            for player_id in self.game.list_owners
        ]

        super().__init__(placeholder="Guess the owner...", min_values=1, max_values=1, options=options)
        

    async def callback(self, interaction: Interaction):
        player_id = interaction.user.id
        owner_guess = int(self.values[0])

        # Store guess in the game session
        await self.game.add_guess(player_id, owner_guess, None)  # category_guess can be added later

        # await interaction.response.send_message(f"Your guess for {self.entry.name} has been submitted.", ephemeral=True)

class CategoryDropdown(ui.Select):
    def __init__(self, game, entry):
        options = [
            SelectOption(label="Favorited", value="True"),
            SelectOption(label="Hated", value="False")
        ]
        super().__init__(placeholder="Guess category...", min_values=1, max_values=1, options=options)
        self.game = game
        self.entry = entry

    async def callback(self, interaction: Interaction):
        player_id = interaction.user.id
        category_guess = self.values[0] == "True"
        await self.game.add_guess(player_id, None, category_guess)
        # await interaction.response.send_message(f"Your category guess has been submitted.", ephemeral=True)