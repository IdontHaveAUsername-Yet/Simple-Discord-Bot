import discord
from discord.ext import commands
import asyncio

# Replace with your bot token
TOKEN = "YourTokenHere"

# Replace with your welcome/goodbye channel ID
WELCOME_GOODBYE_CHANNEL_ID = 123456789012345678

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

bad_words = [
    # Full list of bad words (restored)
]

def is_admin():
    async def predicate(ctx):
        if ctx.author.guild_permissions.administrator:
            return True
        admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
        if admin_role and admin_role in ctx.author.roles:
            return True
        return False
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Bot is online: {bot.user.name}')
    print("███╗░░░███╗░█████╗░██████╗░███████╗  ██████╗░██╗░░░██╗  ███╗░░░███╗██╗░░░██╗░██████╗████████╗██╗░█████╗░")
    print("████╗░████║██╔══██╗██╔══██╗██╔════╝  ██╔══██╗╚██╗░██╔╝  ████╗░████║╚██╗░██╔╝██╔════╝╚══██╔══╝██║██╔══██╗")
    print("██╔████╔██║███████║██║░░██║█████╗░░  ██████╦╝░╚████╔╝░  ██╔████╔██║░╚████╔╝░╚█████╗░░░░██║░░░██║██║░░╚═╝")
    print("██║╚██╔╝██║██╔══██║██║░░██║██╔══╝░░  ██╔══██╗░░╚██╔╝░░  ██║╚██╔╝██║░░╚██╔╝░░░╚═══██╗░░░██║░░░██║██║░░██╗")
    print("██║░╚═╝░██║██║░░██║██████╔╝███████╗  ██████╦╝░░░██║░░░  ██║░╚═╝░██║░░░██║░░░██████╔╝░░░██║░░░██║╚█████╔╝")
    for guild in bot.guilds:
        muted_role = discord.utils.get(guild.roles, name="Muted")
        if not muted_role:
            permissions = discord.Permissions(send_messages=False, speak=False)
            muted_role = await guild.create_role(name="Muted", permissions=permissions)
            for channel in guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        try:
            await message.author.send("No Bad Words :P")
        except discord.Forbidden:
            await message.channel.send(f"{message.author.mention}, please do not use bad words! (I couldn't send you a DM.)")
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_GOODBYE_CHANNEL_ID)
    if channel is None:
        print("Welcome/Goodbye channel not found. Please check the channel ID.")
        return

    embed = discord.Embed(
        title=f"Welcome to the server, {member.name}!",
        description="We're excited to have you here. Please read the rules and enjoy your stay!",
        color=0x00ff00
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"You are our {len(member.guild.members)}th member!")

    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_GOODBYE_CHANNEL_ID)
    if channel is None:
        print("Welcome/Goodbye channel not found. Please check the channel ID.")
        return

    embed = discord.Embed(
        title=f"Goodbye, {member.name}!",
        description="We're sad to see you go. Take care and hope to see you again!",
        color=0xff0000
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"We now have {len(member.guild.members)} members.")

    await channel.send(embed=embed)

@bot.command()
@is_admin()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned. Reason: {reason}")

@bot.command()
@is_admin()
async def unban(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"{user.name}#{user.discriminator} has been unbanned.")
    except discord.NotFound:
        await ctx.send("User not found in the ban list.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to unban this user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to unban the user: {e}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        if ctx.guild.me.top_role <= member.top_role:
            await ctx.send(f"I cannot kick {member.mention} because they have a higher or equal role to me.")
            return

        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick this user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to kick the user: {e}")

@bot.command()
@is_admin()
async def write(ctx, channel_id: int, *, message: str):
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Channel not found. Please check the channel ID.")
        return
    await channel.send(message)
    await ctx.send(f"Message has been sent to {channel.name}.")

@bot.command()
async def poll(ctx, question, *options):
    if len(options) < 1:
        await ctx.send("You need to provide at least one option.")
        return
    if len(options) > 10:
        await ctx.send("You can only provide up to 10 options.")
        return

    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    poll_message = f"**{question}**\n\n"
    for i, option in enumerate(options):
        poll_message += f"{emojis[i]} {option}\n"

    message = await ctx.send(poll_message)
    for i in range(len(options)):
        await message.add_reaction(emojis[i])

@bot.command()
async def embed(ctx, title: str, description: str, color: str = "0x00ff00"):
    """
    Sends a custom embed message with user-defined content.
    Usage: $embed "Title" "Description" [color]
    Example: $embed "My Title" "This is a description" 0xff0000
    """
    try:
        # Convert color from hex string to integer
        embed_color = int(color, 16)
    except ValueError:
        await ctx.send("Invalid color format. Please use a hex color code (e.g., 0x00ff00).")
        return

    # Create the embed
    embed = discord.Embed(
        title=title,
        description=description,
        color=embed_color
    )

    # Add fields dynamically (optional)
    await ctx.send("Would you like to add fields to the embed? (yes/no)")
    response = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if response.content.lower() in ["yes", "y"]:
        while True:
            await ctx.send("Enter field name (or type 'done' to finish):")
            field_name_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            field_name = field_name_msg.content
            if field_name.lower() == "done":
                break
            await ctx.send("Enter field value:")
            field_value_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            field_value = field_value_msg.content
            embed.add_field(name=field_name, value=field_value, inline=False)

    # Add thumbnail (optional)
    await ctx.send("Would you like to add a thumbnail? (yes/no)")
    response = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if response.content.lower() in ["yes", "y"]:
        await ctx.send("Enter thumbnail URL:")
        thumbnail_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        thumbnail_url = thumbnail_msg.content
        embed.set_thumbnail(url=thumbnail_url)

    # Add footer (optional)
    await ctx.send("Would you like to add a footer? (yes/no)")
    response = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if response.content.lower() in ["yes", "y"]:
        await ctx.send("Enter footer text:")
        footer_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        footer_text = footer_msg.content
        embed.set_footer(text=footer_text)

    # Send the embed
    await ctx.send(embed=embed)

@bot.command()
@is_admin()
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("The 'Muted' role does not exist. Please create it manually.")
        return
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

@bot.command()
@is_admin()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("The 'Muted' role does not exist. Please create it manually.")
        return
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted.")

@bot.command()
@is_admin()
async def tempmute(ctx, member: discord.Member, duration: int, *, reason="No reason provided"):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("The 'Muted' role does not exist. Please create it manually.")
        return
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {duration} minutes. Reason: {reason}")
    await asyncio.sleep(duration * 60)
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted after {duration} minutes.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="Here is a list of all available commands and their functions:",
        color=0x00ff00
    )

    embed.add_field(name="$help", value="Displays this help message with all available commands.", inline=False)
    embed.add_field(name="$ban @user [reason]", value="Bans a user from the server. (Admin only)", inline=False)
    embed.add_field(name="$unban user_id", value="Unbans a user by their ID. (Admin only)", inline=False)
    embed.add_field(name="$kick @user [reason]", value="Kicks a user from the server. (Admin only)", inline=False)
    embed.add_field(name="$mute @user [reason]", value="Mutes a user. (Admin only)", inline=False)
    embed.add_field(name="$unmute @user", value="Unmutes a user. (Admin only)", inline=False)
    embed.add_field(name="$tempmute @user duration_in_minutes [reason]", value="Temporarily mutes a user for a specified duration. (Admin only)", inline=False)
    embed.add_field(name="$poll 'question' 'option1' 'option2' ...", value="Creates a poll with up to 10 options.", inline=False)
    embed.add_field(name="$embed 'title' 'description' [color]", value="Sends a custom embed message. Color is optional (e.g., 0x00ff00 for green).", inline=False)
    embed.add_field(name="$write channel_id 'message'", value="Sends a message to a specific channel. (Admin only)", inline=False)

    embed.set_footer(text="Use commands responsibly!")
    await ctx.send(embed=embed)

bot.run(TOKEN)
