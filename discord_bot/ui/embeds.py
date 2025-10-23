from nextcord import Embed
from discord_bot.utils import get_username_from_id
import asyncio

COLOR = 0x2ab4f2

def make_list_embed(favorites, hated):
    embed = Embed(title="Your List", color=COLOR)

    fav_text = "\n".join(favorites) if favorites else "(none yet)"
    hated_text = "\n".join(hated) if hated else "(none yet)"
    
    embed.add_field(name="Favorites", value=fav_text, inline=False)
    embed.add_field(name="Hated", value=hated_text, inline=False)
    
    return embed

def make_confirm_embed(mode, entry):
    embed = Embed(title="Confirm Entry", color=COLOR)

    match mode:
        case "anime":
            pass
        case "character":
            pass
        case _:
            embed.description = entry


    return embed

async def make_game_embed(players: set[int]) -> Embed:
    embed = Embed(title="Game started", color=COLOR)
    
    if players:
        usernames = await asyncio.gather(*(get_username_from_id(p) for p in players))
        player_text = "\n".join(f"@{name}" for name in usernames)
    else:
        player_text = "(none yet)"
    
    embed.add_field(name="Lists Submitted", value=player_text, inline=False)
    return embed

def make_entry_embed(mode, entry):
    embed = Embed(title="Entry", color=COLOR)
    match mode:
        case "anime":
            pass
        case "character":
            pass
        case _:
            embed.description = entry

    return embed
