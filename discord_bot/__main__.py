import discord
from discord.ext import commands
import os
from os.path import join, dirname

from dotenv import load_dotenv

from .cogs.score import Score
from .cogs.remindme import RemindMe, Reminder
from .db import db


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

db.connect()
with db:
    db.create_tables([Reminder])

bot = commands.Bot(command_prefix=".")

bot.add_cog(Score(bot))
bot.add_cog(RemindMe(bot))

bot.run(DISCORD_TOKEN)
