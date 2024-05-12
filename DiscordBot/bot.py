import os
import platform
import logging
import random
import asyncio
from json import load
from pathlib import Path
import discord
from discord.ext import commands, tasks

# Define your list of towns
towns = ["Saint Denis", "Valentine", "Rhodes", "Blackwater", "Strawberry", "Tumbleweed", "Armadillo", "Van Horn", "Annesburg", "Emerald Ranch"]

#interval for changing the presence (in seconds)
change_interval = 6 * 60 * 60

# Fetch bot token.
with Path("../config.json").open() as f:
    config = load(f)


TOKEN = config["DISCORD_TOKEN"]


# DO NOT TOUCH - for running on hosting platform.
if TOKEN == "":
    TOKEN = os.environ.get("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = False

bot = commands.Bot(
    intents=intents
)
# Logging.
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)
# Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            logging.info(f'Loaded {filename[:-3]}')
        except discord.errors.ExtensionFailed as e:
            logging.error(f'Failed to load {filename[:-3]}')
            logging.error(e.with_traceback(e.__traceback__))


async def presence_loop():
    while True:
        # Choose a random town from the list
        town = random.choice(towns)
        # Update the bot's presence
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {town}"))
        # Wait for the specified interval
        await asyncio.sleep(change_interval)


@bot.slash_command(name="ping", description="Pong back latency")
async def ping(ctx: discord.ApplicationContext):
    """Pong back latency"""
    await bot.wait_until_ready()
    await ctx.respond(
        f"_Pong!_ ({round(bot.latency * 1000, 1)} ms)",
        ephemeral=True,
        delete_after=15)
if __name__ == "__main__":
    bot.run(TOKEN, reconnect=True)
