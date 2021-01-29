from collections import defaultdict
import re

import discord
from discord.ext import commands


class Score(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._scores = defaultdict(lambda: 0)

        print("Registered score")

    @commands.Cog.listener()
    async def on_message(self, message):
        for subject in re.findall("(\S+?)\+\+", message.content):
            self._scores[subject] += 1

    @commands.command()
    async def scores(self, ctx):
        for subject, score in self._scores.items():
            await ctx.send(f"{subject}: {score}")
