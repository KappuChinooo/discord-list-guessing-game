import nextcord
from nextcord.ext.commands import Bot
import config

import os
from dotenv import load_dotenv

load_dotenv()

intents = nextcord.Intents.default()
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_IDS = [int(x) for x in os.getenv("GUILD_IDS", "").split(",") if x]

bot = Bot(command_prefix=config.command_prefix, intents=intents, default_guild_ids=GUILD_IDS)

bot.run(TOKEN)
