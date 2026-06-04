import discord
import random
from src import commands

# Events itself

def setup_events(client, tree):
    # Bot starting process

    @client.event
    async def on_ready():
        activities = ["Assisting @4zuj at his work",
                      "Doing Arbeitszeitbetrug in Dorf Schneckenhofen",
                      "Executing commands in @4zuj his server",
                      "Deep diving into the server audit-logs :D",
                      ":D!",
                      "https://linktr.ee/4zuj"]

        await tree.sync()
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(activities)))
        print(f"\nLogged in as {client.user}")

    # Voice chat join, switch and leave logger

    @client.event
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        display_name = member.name
        display_avatar = member.display_avatar.url
        member_id = member.id
        get_channel = client.get_channel(commands.voice_state_channel)

        if not before.channel:
            embed = discord.Embed(color=0x2FC24D)
            embed.set_author(name=display_name, icon_url=display_avatar)
            embed.add_field(name="", value=f"{member.mention} joined voice channel {after.channel.mention}")
            embed.set_footer(text=f"UID: {member_id} at {commands.get_current_time()}")
            await get_channel.send(embed=embed)

        elif not after.channel:
            embed = discord.Embed(color=0xC22F2F)
            embed.set_author(name=display_name, icon_url=display_avatar)
            embed.add_field(name="", value=f"{member.mention} left voice channel {before.channel.mention}")
            embed.set_footer(text=f"UID: {member_id} at {commands.get_current_time()}")
            await get_channel.send(embed=embed)

        elif not before.channel == after.channel:
            embed = discord.Embed(color=0x2FC24D)
            embed.set_author(name=display_name, icon_url=display_avatar)
            embed.add_field(name="", value=f"{member.mention} switched voice channels from {before.channel.mention} to {after.channel.mention}")
            embed.set_footer(text=f"UID: {member_id} at {commands.get_current_time()}")
            await get_channel.send(embed=embed)

    # Deleted or edited Message logger

    @client.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        display_name = before.author.name
        display_avatar = before.author.display_avatar.url
        member_id = before.author.id
        get_channel = client.get_channel(commands.message_change_channel)

        embed = discord.Embed(color=0x1c1e1d)
        embed.set_author(name=display_name, icon_url=display_avatar)
        if before.content == after.content:
            return
        else:
            embed.add_field(name=f"Message Edited in {before.channel.mention} Jump to message -> {before.jump_url}",
                            value="")
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.set_footer(text=f"UID: {member_id} at {commands.get_current_time()}")

            if before.author.bot:
                return
            else:
                await get_channel.send(embed=embed)
            return

    @client.event
    async def on_message_delete(message: discord.Message):
        display_name = message.author.name
        display_avatar = message.author.display_avatar
        member_id = message.author.id
        get_channel = client.get_channel(commands.message_change_channel)

        embed = discord.Embed(color=0xC22F2F)
        embed.set_author(name=display_name, icon_url=display_avatar)
        if message.attachments:
            embed.add_field(name="",
                            value=f"Attachment sent by {message.author.mention} deleted in {message.channel.mention} \n{message.attachments[0]}")
        elif message.content:
            embed.add_field(name="",
                            value=f"Message sent by {message.author.mention} deleted in {message.channel.mention} \n{message.content}")
        embed.set_footer(text=f"UID: {member_id} at {commands.get_current_time()}")

        if not message.author.bot:
            if message.guild:
                await get_channel.send(embed=embed)
            else:
                return
        return

    # Returning the message of a user, when the bots receives a dm

    @client.event
    async def on_message(message: discord.Message):
        if not message.author.bot:
            if not message.guild:
                dm_user_id = message.author.id
                dm_user_name = message.author.name
                dm_user_avatar = message.author.display_avatar
                dm_message = message.content
                get_channel = client.get_channel(commands.dm_bot_history_channel)

                embed = discord.Embed(color=0x2FC24D)
                embed.set_author(name=dm_user_name, icon_url=dm_user_avatar.url)
                embed.add_field(name=f"Received direct-message", value=f"from {message.author.mention}")
                embed.add_field(name="Message", value=f"{dm_message}", inline=False)
                embed.set_footer(text=f"UID: {dm_user_id} at {commands.get_current_time()}")

                await get_channel.send(embed=embed)
            else:
                return
        else:
            return
