import nextcord
from nextcord.ext.commands import Bot
import config

intents = nextcord.Intents.default()
intents.message_content = True


bot = Bot(command_prefix=config.command_prefix, intents=intents, default_guild_ids=config.GUILD_IDS)

bot.run(config.TOKEN)
