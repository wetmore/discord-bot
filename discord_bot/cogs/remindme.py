from collections import defaultdict
from datetime import datetime
import re

import discord
from discord.ext import tasks, commands
from parsedatetime import Calendar
from peewee import *
from pytz import timezone

from ..db import BaseModel, TimestampTzField


def get_time(time_string):
    cal = Calendar()
    now = datetime.now(timezone("UTC"))

    if time_string == "":
        time = cal.parseDT("1 day", now)
    else:
        time = cal.parseDT(time_string, now)

    return time[0]


class Reminder(BaseModel):
    time = TimestampTzField()
    user_id = IntegerField()
    message_id = IntegerField()
    channel_id = IntegerField()
    reminder_text = CharField()


class RemindMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        print("Registered remindme")
        self.poll.start()

    def cog_unload(self):
        self.poll.cancel()

    @tasks.loop(seconds=60.0)
    async def poll(self):
        cal = Calendar()

        now = datetime.now(timezone("UTC"))
        then = cal.parseDT("1 minute", now)

        print("polling...")
        for r in Reminder.select().where(Reminder.time.between(now, then[0])):
            await self.bot.get_channel(r.channel_id).send(r.reminder_text)

    @commands.command()
    async def remindme(self, ctx, *, arg):
        """
        Set a reminder for yourself
        """
        match = re.match('(.*?)"(.+?)"', arg)

        if match:
            time = get_time(match.group(1))
            reminder_text = match.group(2)

        Reminder.create(
            time=time,
            user_id=ctx.author.id,
            message_id=ctx.message.id,
            reminder_text=reminder_text,
            channel_id=ctx.channel.id,
        )

    @commands.command()
    async def reminders(self, ctx):
        reply = ""

        for reminder in Reminder.select():
            reply += f"{reminder.reminder_text} at {reminder.time}\n"

        await ctx.send(reply)
