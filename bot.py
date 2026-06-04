# Imports

import discord
from discord import app_commands
from src import commands, events, database

# Variables

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Loading functions

database.create_warn_database(commands.orbis_database)
commands.setup_commands(tree, client)
events.setup_events(client, tree)

# Discord-bot setup

client.run(commands.discord_bot_token)