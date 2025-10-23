
import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_IDS = [int(x) for x in os.getenv("GUILD_IDS", "").split(",") if x]

command_prefix = ('Kappu ', 'kappu ')
can_score_on_own_list = False

OWNER_CORRECT_POINTS = 1
BOTH_CORRECT_POINTS = 1