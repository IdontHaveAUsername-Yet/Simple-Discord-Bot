import discord
from discord.ext import commands
import asyncio

# Replace with your bot token
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Replace with your welcome/goodbye channel ID
WELCOME_GOODBYE_CHANNEL_ID = 123456789012345678

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

bad_words = [
    "idiot", "moron", "retard", "dumbass", "asshole", "arsehole", "asshat", "assclown",
    "son of a bitch", "bitch", "bastard", "motherfucker", "nigga", "nga", "nig", "n-word",
    "dickhead", "dick", "dickface", "dickwad", "cunt", "cuntface", "cuntbag", "shit",
    "shithead", "shitface", "fuck", "fucker", "fuckface", "fuckboy", "pussy", "puss",
    "pussbag", "douchebag", "douche", "douchecanoe", "fucktard", "fuckwit", "shitstain",
    "scumbag", "twat", "wanker", "bellend", "knobhead", "knob", "tosser", "wankstain",
    "fucknugget", "dipshit", "shitbag", "shitforbrains", "arschloch", "arsch", "arschgeige",
    "arschkrampe", "arschlecker", "hurensohn", "hurenkind", "hurentochter", "hurenbengel",
    "idiot", "idiotenkind", "vollidiot", "blödmann", "wichser", "wichsbeutel", "wichsgesicht",
    "trottel", "volltrottel", "dummkopf", "depp", "volldepp", "deppert", "scheiße",
    "scheißkerl", "scheißtyp", "mistkerl", "miststück", "mistvieh", "fotze", "fotzenkind",
    "fotzengesicht", "schwanz", "schwanzlutscher", "schwanzkopf", "sackgesicht", "hirni",
    "hirnlos", "spast", "spacko", "vollpfosten", "armleuchter", "dummbeutel", "sack",
    "sackratte", "vollassi", "vollhonk", "vollspast", "volltussi", "idiota", "imbécil",
    "estúpido", "cabrón", "cabronazo", "cabroncete", "pendejo", "pendejada", "pendejete",
    "hijo de puta", "puta", "puto", "mierda", "mierdoso", "mierdero", "gilipollas",
    "gilipuertas", "gilipollismo", "coño", "coñazo", "coñito", "maricón", "marica",
    "mariconazo", "zorra", "zorrón", "zorrupia", "joder", "jodido", "jodete", "connard",
    "connasse", "con", "salaud", "salope", "salopard", "enculé", "enculeur", "enculage",
    "fils de puta", "pute", "putain", "merde", "merdeux", "merdier", "crétin", "crétinisme",
    "crétinerie", "débile", "débilos", "débilité", "trou du cul", "trouduc", "trouducologie",
    "nique", "niquer", "niqueur", "batard", "batarde", "batardise", "идиот", "идиотина",
    "идиотство", "дурак", "дурачок", "дурачина", "ублюдок", "ублюдство", "сволочь",
    "сволочной", "сука", "сукин", "сучара", "мразь", "мразота", "дебил", "дебильность",
    "тварь", "тварюка", "козёл", "козлина", "чмо", "чмок", "أحمق", "حمقى", "كلب", "كلاب",
    "ابن الكلب", "ابن كلب", "حمار", "حمير", "عاهرة", "عاهرات", "قذر", "قذارة", "خنزير",
    "خنازير", "ولد الزنا", "زنا", "مجنون", "جنون", "كس أمك", "كس", "白痴", "白痴儿", "笨蛋",
    "笨", "混蛋", "混球", "傻瓜", "傻逼", "蠢货", "蠢", "王八蛋", "王八", "狗屎", "狗", "神经病",
    "神经", "贱人", "贱", "畜生", "畜", "バカ", "馬鹿", "バカ野郎", "アホ", "阿呆", "クソ", "糞",
    "畜生", "ちくしょう", "ドジ", "ドジっ子", "変態", "へんたい", "ゴミ", "ごみ", "クズ", "くず",
    "死ね", "しね", "ブス", "ぶす"
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
async def embed(ctx, title, description, color="0x00ff00"):
    embed = discord.Embed(
        title=title,
        description=description,
        color=int(color, 16)
    )
    embed.add_field(name="Field 1", value="This is the first field.", inline=False)
    embed.add_field(name="Field 2", value="This is the second field.", inline=True)
    embed.set_thumbnail(url="https://example.com/image.png")
    embed.set_footer(text="This is the footer.")
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
