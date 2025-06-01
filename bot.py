# bot.py

import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

# Load environment variables (DISCORD_TOKEN and TEST_GUILD_ID)
load_dotenv()
discordToken = getenv("DISCORD_TOKEN")
testGuildID = getenv("GUILD_ID")

if discordToken is None:
    raise ValueError("No token found in environment variable DISCORD_TOKEN")
if testGuildID is None:
    raise ValueError("No guild ID found in environment variable TEST_GUILD_ID")

# Set up bot with required intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Set up slash command tree
@bot.event
async def on_ready():
    guild = discord.Object(id=int(testGuildID))  # Create guild object from ID
    await bot.tree.sync(guild=guild)  # Sync commands to that test server only
    print(f"Logged in as {bot.user} and synced commands to guild {testGuildID}")

# Define a slash command
@bot.tree.command(name="hello", description="Says hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, world!")

# Run the bot
bot.run(discordToken)
