from nextcord import ui, Interaction, TextInputStyle
from nextcord import ButtonStyle
from game.game import GameSession
from discord_bot.ui.embeds import make_list_embed, make_confirm_embed, make_game_embed
import asyncio
import nextcord

class ListMenu(ui.View):
    def __init__(self, user_id, game: GameSession):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.favorites = []
        self.hated = []
        self.game = game
        self.submitted = False
        self.list_message = None
        self.game_message = None
        self.mode = game.mode
        self.fav_num = game.fav_num
        self.hated_num = game.hated_num

    @ui.button(label="Add Favorite", style=ButtonStyle.blurple)
    async def add_fav(self, button: ui.Button, interaction: Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your list.", ephemeral=True)
            return
        if len(self.favorites) >= self.fav_num:
            await interaction.response.send_message("You already have the maximum numbers of favorites.", ephemeral=True)
            return
        await interaction.response.send_modal(AddEntryModal(self, is_favorite=True, mode=self.mode))    

    @ui.button(label="Add Hated", style=ButtonStyle.red)
    async def add_hated(self, button: ui.Button, interaction: Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your list.", ephemeral=True)
            return
        if len(self.favorites) >= self.hated_num:
            await interaction.response.send_message("You already have the maximum numbers of hated.", ephemeral=True)
            return
        await interaction.response.send_modal(AddEntryModal(self, is_favorite=False, mode=self.mode))    

    @ui.button(label="Finish", style=ButtonStyle.gray)
    async def finish(self, button: ui.Button, interaction: Interaction):
        if self.game is None:
            return
        if self.game.current_entry:
            await interaction.response.send_message("Game has already started.", ephemeral=True)
            return

        if self.submitted:
            await interaction.response.send_message("You already submitted your list.", ephemeral=True)
            return
        self.submitted = True
        
        if len(self.favorites) == 0 or len(self.hated) == 0:
            await interaction.response.send_message("You can not have an empty list.", ephemeral=True)
            return

        for fav in self.favorites:
            await self.game.submit_entry(self.user_id, fav, True)        
        for hate in self.hated:
            await self.game.submit_entry(self.user_id, hate, False)
        await interaction.response.edit_message(view=None)
        await interaction.followup.send("Your list has been submitted.", ephemeral=True)

        embed = await make_game_embed(self.game.list_owners)
        await self.game_message.edit(embed=embed)


    async def update_embed(self):
        embed = make_list_embed(self.favorites, self.hated)
        await self.list_message.edit(embed=embed, view=self)



class AddEntryModal(ui.Modal):
    def __init__(self, menu: ListMenu, is_favorite: bool, mode: str):
        super().__init__(title="Add Entry", timeout=None)
        self.menu = menu
        self.is_favorite = is_favorite
        self.mode = mode

        self.entry_name = ui.TextInput(
            label="Entry Name",
            style=TextInputStyle.short
        )
        self.add_item(self.entry_name)

    
    async def callback(self, interaction: Interaction):
        entry = self.entry_name.value
        if not entry.strip():
            await interaction.response.send_message("Entry cannot be empty.", ephemeral=True)
            return
        
        confirm_view = ConfirmEntryView(self.menu, self.entry_name.value, self.is_favorite, self.mode)
        confirm_embed = make_confirm_embed(self.mode, self.entry_name.value)
        await interaction.response.send_message(embed=confirm_embed, view=confirm_view, ephemeral=True)



class ConfirmEntryView(ui.View):
    def __init__(self, menu: ListMenu, entry, is_favorite, mode):
        super().__init__(timeout=60)
        self.menu = menu
        self.entry = entry
        self.is_favorite = is_favorite
        self.mode = mode

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, interaction: Interaction):
        if self.is_favorite:
            self.menu.favorites.append(self.entry)
        else:
            self.menu.hated.append(self.entry)
        await self.menu.update_embed()
        await interaction.response.edit_message(content="Entry added to list.", view=None, embed=None)
        asyncio.create_task(self.dismiss(interaction))


    @ui.button(label="Cancel", style=ButtonStyle.green)
    async def cancel(self, button: ui.Button, interaction: Interaction):
        await interaction.response.edit_message(content="Entry submission canceled.", view=None, embed=None)
        asyncio.create_task(self.dismiss(interaction))

    async def dismiss(self, interaction: Interaction):
        await asyncio.sleep(3)
        try:
            # This works for ephemeral messages
            msg = await interaction.original_response()
            await msg.edit(content=" ", view=None, embed=None)
        except nextcord.NotFound:
            # message already gone / expired
            pass
        except Exception:
            pass