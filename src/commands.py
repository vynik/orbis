import discord
from discord import app_commands
import asyncio
import requests
import random
import json
from datetime import datetime
from src import database

# Functions for the commands

def get_current_time():
    current_time = datetime.now().strftime("%H:%M")
    return current_time

# Token, Api-key and channelids

with open("config.json") as file:
    load_config = json.load(file)

    orbis_database = load_config["database"][0]["name"]

    discord_bot_token = load_config["tokens"][0]["discord_token"]
    giphy_token = load_config["tokens"][0]["giphy_api"]

    voice_state_channel = load_config["channels"][0]["vc-join-leave-log_id"]
    dm_bot_history_channel = load_config["channels"][0]["dm-bot-history_id"]
    message_change_channel = load_config["channels"][0]["message-del-or-edit-log_id"]
    bot_message_history_channel = load_config["channels"][0]["bot-message-sent-log_id"]
    warn_log_channel = load_config["channels"][0]["warn-logs_id"]
    ticket_history_channel = load_config["channels"][0]["ticket-history_id"]

    ticket_category_id = load_config["categories"][0]["ticket-category_id"]

# Commands itself

def setup_commands(tree, client):
    # Staff commands

    @tree.command(name="warn_user", description="Warn any user in the server.")
    @app_commands.describe(member="What user do you want to warn?", reason="For what reason are you warning the user?", duration="For how long is the warn applied for? You may enter the correct time e.g. 120d", appealable="Is the warn appealable?", evidence="Insert here a screenshot link (you don't have to, you can also just let this empty.)")
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.guild_only()
    async def warn(interaction: discord.Interaction, member: discord.Member, reason: str, duration: str, appealable: bool, evidence: str):
        staff_name = interaction.user.name
        staff_avatar = interaction.user.display_avatar
        staff_id = interaction.user.id
        get_channel = client.get_channel(warn_log_channel)
        get_server_name = interaction.guild

        embed_log = discord.Embed(color=0x1c1e1d)
        embed_log.set_author(name=staff_name, icon_url=staff_avatar)
        embed_log.add_field(name="", value=f"The user {member.mention} has been successfully warned by {interaction.user.mention} for {duration}!", inline=False)
        embed_log.add_field(name="Reason", value=reason, inline=False)
        if "https://" in evidence:
            embed_log.add_field(name="Evidence", value=evidence, inline=False)
        else:
            evidence = "-"
            embed_log.add_field(name="Evidence", value="Not provided or wrongly inserted.")
        embed_log.set_footer(text=f"UID: {staff_id} at {get_current_time()}")

        embed_warn_message = discord.Embed(color=0xC22F2F)
        embed_warn_message.set_author(name="", icon_url="https://cdn.discordapp.com/attachments/1499696673528746145/1502029774787448962/hammer.png?ex=69fe39bc&is=69fce83c&hm=b23d08409eb3fc119c7dd4377bc05366becf20e9b4419beaf0e98dc415dab416&")
        embed_warn_message.add_field(name=f"Oh no! You have been warned by {staff_name} in the Server: {get_server_name}!", value=f"**Reason:** {reason}\n**Duration:** {duration}\n**Appealable:** {appealable}")
        embed_warn_message.set_footer(text="If you would like to appeal the warn, please write @4zuj or do /createticket via discord for more information.")

        database.log_warn(orbis_database, member.name, member.id, interaction.user.name, reason, duration, evidence, appealable)

        await get_channel.send(embed=embed_log)
        try:
            await member.send(embed=embed_warn_message)
            await interaction.response.send_message("The user has been warned successfully!", ephemeral=True)
        except:
            await interaction.response.send_message(f"The user {member.mention} you have warned, wasn't able to receive a message.", ephemeral=True)

    @tree.command(name="warn_logs", description="Get all current existing warns of a user!")
    @app_commands.describe(member="From what user would you like to see all active warns?")
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.guild_only()
    async def read_warns(interaction: discord.Interaction, member: discord.Member):
        get_channel = interaction.channel
        get_user_id = member.id
        rows = database.read_database(orbis_database, get_user_id)

        await interaction.response.send_message(f"Loading the active warns of the user {member.mention} now!", ephemeral=True)

        for id, member, member_id, warned_by, reason, duration, evidence, appealable in rows:
            await get_channel.send(f"**WarnID:** {id}\n**Username:** {member}\n**UserID:** {member_id}\n**Warned by:** {warned_by}\n**Reason:** {reason}\n**Duration:** {duration}\n**Evidence:** {evidence}\n**Appealable?:** {appealable}\n")

    @tree.command(name="warn_archive_logs", description="Get all archived existing warns. (WARNING!: THIS COULD CAUSE PROBLEMS IF YOU HAVE MANY WARNS)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def read_archived_warns(interaction: discord.Interaction):
        get_channel = interaction.channel
        rows = database.read_archive_database(orbis_database)

        await interaction.response.send_message("Loading all warns now!", ephemeral=True)

        for id, member, member_id, warned_by, reason, duration, evidence, appealable in rows:
            await get_channel.send(f"**WarnID:** {id}\n**Username:** {member}\n**UserID:** {member_id}\n**Warned by:** {warned_by}\n**Reason:** {reason}\n**Duration:** {duration}\n**Evidence:** {evidence}\n**Appealable?:** {appealable}\n")

    @tree.command(name="remove_warn", description="Remove a warn from the database")
    @app_commands.describe(warn_id="What warn id would you like to delete?")
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.guild_only()
    async def warn_remove(interaction: discord.Interaction, warn_id: int):
        display_name = interaction.user.name
        display_avatar = interaction.user.display_avatar
        staff_id = interaction.user.id
        get_channel = client.get_channel(warn_log_channel)
        rows = database.read_deleted_warn(orbis_database, warn_id)

# wenn keine richtige id angegeben wird, crasht der code....

        for id, member, member_id, warned_by, reason, duration, evidence, appealable in rows:
            content = f"**WarnID:** {id}\n**Username:** {member}\n**UserID:** {member_id}\n**Warned by:** {warned_by}\n**Reason:** {reason}\n**Duration:** {duration}\n**Evidence:** {evidence}\n**Appealable?:** {appealable}\n"

        embed = discord.Embed()
        embed.set_author(name=display_name, icon_url=display_avatar)
        embed.add_field(name=f"has deleted the warn with the ID {warn_id}!", value="")
        embed.add_field(name=f"Content of the warning", value=content, inline=False)
        embed.set_footer(text=f"UID: {staff_id} at {get_current_time()}")

        database.delete_warn(orbis_database, warn_id)
        await interaction.response.send_message(f"Removing warn with the ID: {warn_id}!", ephemeral=True)
        await get_channel.send(embed=embed)

    @tree.command(name="purge", description="Delete many messages at a time!")
    @app_commands.describe(amount_of_deleting_messages="How many messages would you like to delete? (max 100)", reason="Why would you like to delete this many amount of messages?")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def purge(interaction: discord.Interaction, amount_of_deleting_messages: int, reason: str):
        display_name = interaction.user.name
        display_avatar = interaction.user.display_avatar
        member_id = interaction.user.id
        get_channel = client.get_channel(message_change_channel)

        if amount_of_deleting_messages < 1 or amount_of_deleting_messages > 100:
            await interaction.response.send_message(content="The amount you've entered in isn't valid 😡.", ephemeral=True)
        else:
            embed = discord.Embed(color=0x1c1e1d)
            embed.set_author(name=display_name, icon_url=display_avatar)
            if amount_of_deleting_messages >= 2:
                embed.add_field(name=f"has purged {amount_of_deleting_messages} messages in {interaction.channel.mention}", value="")
                await interaction.response.send_message(f"purging {amount_of_deleting_messages} messages!", ephemeral=True)
            else:
                embed.add_field(name=f"has purged {amount_of_deleting_messages} message in {interaction.channel.mention}", value="")
                await interaction.response.send_message(f"purging successfully {amount_of_deleting_messages} message!", ephemeral=True)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.set_footer(text=f"UID: {member_id} at {get_current_time()}")
            await interaction.channel.purge(limit=amount_of_deleting_messages)
            await get_channel.send(embed=embed)

    @tree.command(name="send_message", description="Send a message with Orbis!")
    @app_commands.describe(channel="The channel where you would like to type in", message="What would you like Orbis to write?")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def send_message(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        display_name = interaction.user.name
        display_avatar = interaction.user.display_avatar
        member_id = interaction.user.id
        get_channel = client.get_channel(channel.id)
        get_log_channel = client.get_channel(bot_message_history_channel)

        embed = discord.Embed(color=0x1c1e1d)

        embed.set_author(name=display_name, icon_url=display_avatar)
        embed.add_field(name=f"sent a message as Orbis", value=f"**Orbis said:**\n{message}")
        embed.set_footer(text=f"UID: {member_id} at {get_current_time()}")

        await interaction.response.send_message(f"Sent successfully a message in the channel {get_channel.mention}", ephemeral=True)
        await get_log_channel.send(embed=embed)
        await get_channel.send(message)

    @tree.command(name="reply_dm", description="Reply to a dm with Orbis!")
    @app_commands.describe(user="What user would you like to send a message to?", reply="What would you like Orbis to reply?")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def reply_dm(interaction: discord.Interaction, user: discord.Member, reply: str):
        display_name = interaction.user.name
        display_avatar = interaction.user.display_avatar
        member_id = interaction.user.id
        get_log_channel = client.get_channel(bot_message_history_channel)

        embed = discord.Embed(color=0x1c1e1d)
        embed.set_author(name=display_name, icon_url=display_avatar)
        embed.add_field(name="", value=f"**Orbis replied to {user}:**\n{reply}")
        embed.set_footer(text=f"UID: {member_id} at {get_current_time()}")

        await interaction.response.send_message(f"Replied successfully to {user.mention}!", ephemeral=True)
        await get_log_channel.send(embed=embed)
        try:
            await user.send(f"**Reply from {display_name}:** {reply}")
        except:
            await interaction.response.send_message(f"The user {member.mention} you have sending a message, wasn't able to receive a message.", ephemeral=True)

    # Support commands

    @tree.command(name="createticket", description="Create's a ticket!")
    @app_commands.guild_only()
    async def create_ticket(interaction: discord.Interaction):
        display_name = interaction.user
        display_avatar = interaction.user.display_avatar.url
        member_id = interaction.user.id

        category = interaction.guild.get_channel(ticket_category_id)
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                      interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                      interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)}
        new_ticket = await category.create_text_channel(f"Ticket from {display_name}", overwrites=overwrites)

        embed = discord.Embed(color=0x1c1e1d)
        embed.set_author(name=f"New Ticket from {display_name}!", icon_url=display_avatar)
        embed.add_field(name="", value=f"You may now describe your problem, else this ticket is getting closed, {display_name.mention}!")
        embed.set_footer(text=f"UID: {member_id}")
        await interaction.response.send_message(f"Created ticket: {new_ticket.mention}", ephemeral=True)
        await new_ticket.send(embed=embed)
        await asyncio.sleep(delay=0)

    @tree.command(name="closeticket", description="Closes a ticket!")
    @app_commands.describe(user="Who created this ticket you would like to close?", reason="Reason for closing this ticket.")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def delete_ticket(interaction: discord.Interaction, user: discord.Member, reason: str):
        staff_name = interaction.user.name
        staff_avatar = interaction.user.display_avatar
        staff_id = interaction.user.id
        get_channel = client.get_channel(ticket_history_channel)
        get_server_name = interaction.guild

        embed_log = discord.Embed(color=0x1c1e1d)
        embed_log.set_author(name=staff_name, icon_url=staff_avatar)
        embed_log.add_field(name="", value=f"The user {user.mention} his ticket got closed by {interaction.user.mention}", inline=False)
        embed_log.add_field(name="Reason", value=reason, inline=False)
        embed_log.set_footer(text=f"UID: {staff_id} at {get_current_time()}")

        embed_warn_message = discord.Embed(color=0xC22F2F)
        embed_warn_message.set_author(name="", icon_url="https://cdn.discordapp.com/attachments/1499696673528746145/1502029774787448962/hammer.png?ex=69fe39bc&is=69fce83c&hm=b23d08409eb3fc119c7dd4377bc05366becf20e9b4419beaf0e98dc415dab416&")
        embed_warn_message.add_field(name=f"Your ticket has been closed by the staff @{staff_name} in the Server: {get_server_name}!", value=f"**Reason:** {reason}")
        embed_warn_message.set_footer(text="If you think the ticket got closed falsely, please contact @4zuj via discord for more information.")

        await interaction.response.send_message("The user's ticket has been closed successfully!", ephemeral=True)
        await get_channel.send(embed=embed_log)
        try:
            await user.send(embed=embed_warn_message)
        except:
            await interaction.response.send_message(f"The user {member.mention} you tried sending a message, wasn't able to receive a message.", ephemeral=True)
        await interaction.channel.delete()

    @tree.command(name="openticketfor", description="Create's a ticket for a user!")
    @app_commands.describe(user="For what user would you like to create this ticket for", reason="Reason for creating this ticket.")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def open_ticket(interaction: discord.Interaction, user: discord.Member, reason: str):
        display_name = interaction.user
        display_avatar = interaction.user.display_avatar.url
        member_id = interaction.user.id

        category = interaction.guild.get_channel(ticket_category_id)
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                      user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                      user.guild: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                      interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                      interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)}
        new_ticket = await category.create_text_channel(f"Ticket for {user}", overwrites=overwrites)

        embed = discord.Embed(color=0x1c1e1d)
        embed.set_author(name=f"A ticket was created by {display_name} for the user {user}!", icon_url=display_avatar)
        embed.add_field(name="", value=f"This ticket was created by: {display_name.mention}")
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"UID: {member_id} at {get_current_time()}")
        await interaction.response.send_message(f"Created ticket: {new_ticket.mention}", ephemeral=True)
        await new_ticket.send(embed=embed)
        await asyncio.sleep(delay=0)

    # General commands

    @tree.command(name="ping", description="Test the response time!")
    async def ping(interaction: discord.Interaction):
        latency = round(client.latency * 1000)
        await interaction.response.send_message(f"Pong! Responded to {interaction.user.mention} in {latency} ms")

    @tree.command(name="userinfo", description="Get informations about ANY user!")
    @app_commands.describe(user="User to get info about")
    async def userinfo(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(title=f"User Info - `{user.name}`", color=user.color)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Displayname", value=user.display_name)
        embed.add_field(name="Account creation date", value=user.created_at.strftime("%d/%m/%Y at %H:%M"), inline=False)
        embed.set_footer(text=f"User information requested by: {interaction.user.name}\nUID: {interaction.user.id} at {get_current_time()}")

        await interaction.response.send_message(embed=embed)

    @tree.command(name="random_gif", description="Generate a random gif!")
    @app_commands.describe(query="Query you would like to generate a gif about")
    async def random_gif(interaction: discord.Interaction, query: str):
        request = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={giphy_token}&q={query}&limit=25&offset=0&rating=g&lang=en&bundle=messaging_non_clips").json()
        random_gif = random.choice(request["data"])

        try:
            await interaction.response.send_message(random_gif["images"]["original"]["url"])
        except:
            await interaction.response.send_message("An error has occurred...", emphemeral=True)

