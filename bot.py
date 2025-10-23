import nextcord
from nextcord.ext.commands import Bot
import config
from discord_bot.game_cog import GameCog
from game.state import ChannelStateManager
from discord_bot import utils

intents = nextcord.Intents.default()
intents.message_content = True

state_manager = ChannelStateManager()

bot = Bot(command_prefix=config.command_prefix, intents=intents, default_guild_ids=config.GUILD_IDS)

bot.add_cog(GameCog(bot, state_manager))
utils.bot = bot

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")
    for guild_id in config.GUILD_IDS:
        await bot.sync_application_commands(guild_id=guild_id)
        print(f"synced {guild_id}")

bot.run(config.TOKEN)
