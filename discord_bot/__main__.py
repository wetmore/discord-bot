import discord
from discord.ext import commands

from .cogs.score import Score
from .cogs.remindme import RemindMe, Reminder

from .db import db

db.connect()
with db:
    db.create_tables([Reminder])

bot = commands.Bot(command_prefix=".")

bot.add_cog(Score(bot))
bot.add_cog(RemindMe(bot))

bot.run("ODAzNDExMTk4NzA4MDIzMzM3.YA9Y_A.coixmJ28YTKioRtqZQSJJb9UFZc")
