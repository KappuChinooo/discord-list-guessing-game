import nextcord

# global bot reference (assign this from your main bot file)
bot: nextcord.Client  # type hint only

async def get_username_from_id(user_id: int) -> str:
    """
    Get Discord username from user ID.
    Tries cache first (fast), falls back to API fetch if needed.
    Returns 'Unknown(<id>)' if the user cannot be found.
    """
    # Try cache first
    user = bot.get_user(user_id)
    if user:
        return user.name  # cached, no API call needed

    # Fallback: fetch from Discord API
    try:
        user = await bot.fetch_user(user_id)
        return user.name
    except (nextcord.NotFound, nextcord.HTTPException):
        return user_id