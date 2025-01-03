import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Create a bot client with command prefix
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content
bot = commands.Bot(command_prefix="$", intents=intents)

# List of bad words and their variations
bad_words = [
    # English
    "idiot", "moron", "retard", "dumbass",
    "asshole", "arsehole", "asshat", "assclown",
    "son of a bitch", "bitch", "bastard", "motherfucker",
    "nigga", "nga", "nig", "n-word",
    "dickhead", "dick", "dickface", "dickwad",
    "cunt", "cuntface", "cuntbag",
    "shit", "shithead", "shitface",
    "fuck", "fucker", "fuckface", "fuckboy",
    "pussy", "puss", "pussbag",
    "douchebag", "douche", "douchecanoe",

    # German
    "arschloch", "arsch", "arschgeige", "arschkrampe", "arschlecker",
    "hurensohn", "hurenkind", "hurentochter", "hurenbengel",
    "idiot", "idiotenkind", "vollidiot", "blödmann",
    "wichser", "wichsbeutel", "wichsgesicht",
    "trottel", "volltrottel", "dummkopf",
    "depp", "volldepp", "deppert",
    "scheiße", "scheißkerl", "scheißtyp",
    "mistkerl", "miststück", "mistvieh",
    "fotze", "fotzenkind", "fotzengesicht",
    "schwanz", "schwanzlutscher", "schwanzkopf",

    # Spanish
    "idiota", "imbécil", "estúpido",
    "cabrón", "cabronazo", "cabroncete",
    "pendejo", "pendejada", "pendejete",
    "hijo de puta", "puta", "puto",
    "mierda", "mierdoso", "mierdero",
    "gilipollas", "gilipuertas", "gilipollismo",
    "coño", "coñazo", "coñito",
    "maricón", "marica", "mariconazo",
    "zorra", "zorrón", "zorrupia",
    "joder", "jodido", "jodete",

    # French
    "connard", "connasse", "con",
    "salaud", "salope", "salopard",
    "enculé", "enculeur", "enculage",
    "fils de pute", "pute", "putain",
    "merde", "merdeux", "merdier",
    "crétin", "crétinisme", "crétinerie",
    "débile", "débilos", "débilité",
    "trou du cul", "trouduc", "trouducologie",
    "nique", "niquer", "niqueur",
    "batard", "batarde", "batardise",

    # Russian
    "идиот", "идиотина", "идиотство",
    "дурак", "дурачок", "дурачина",
    "ублюдок", "ублюдство",
    "сволочь", "сволочной",
    "сука", "сукин", "сучара",
    "мразь", "мразота",
    "дебил", "дебильность",
    "тварь", "тварюка",
    "козёл", "козлина",
    "чмо", "чмок",

    # Arabic
    "أحمق", "حمقى",
    "كلب", "كلاب",
    "ابن الكلب", "ابن كلب",
    "حمار", "حمير",
    "عاهرة", "عاهرات",
    "قذر", "قذارة",
    "خنزير", "خنازير",
    "ولد الزنا", "زنا",
    "مجنون", "جنون",
    "كس أمك", "كس",

    # Chinese (Mandarin)
    "白痴", "白痴儿",
    "笨蛋", "笨",
    "混蛋", "混球",
    "傻瓜", "傻逼",
    "蠢货", "蠢",
    "王八蛋", "王八",
    "狗屎", "狗",
    "神经病", "神经",
    "贱人", "贱",
    "畜生", "畜",

    # Japanese
    "バカ", "馬鹿", "バカ野郎",
    "アホ", "阿呆",
    "クソ", "糞",
    "畜生", "ちくしょう",
    "ドジ", "ドジっ子",
    "変態", "へんたい",
    "ゴミ", "ごみ",
    "クズ", "くず",
    "死ね", "しね",
    "ブス", "ぶす",
]

# Function to check permissions (admins only)
def is_admin():
    async def predicate(ctx):
        # Check if the user has administrator permissions
        if ctx.author.guild_permissions.administrator:
            return True
        # Optional: Check if the user has a specific role (e.g., "Admin")
        admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
        if admin_role and admin_role in ctx.author.roles:
            return True
        return False
    return commands.check(predicate)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Bot is online: {bot.user.name}')

# Event: Message is sent
@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    # Check if the message contains a bad word
    if any(word in message.content.lower() for word in bad_words):
        # Delete the message
        await message.delete()
        # Send a private warning to the user
        try:
            await message.author.send("Please avoid using inappropriate language.")
        except discord.Forbidden:
            # If the user does not allow DMs, send a message in the channel
            await message.channel.send(f"{message.author.mention}, please do not use bad words! (I couldn't send you a DM.)")

    # Process commands
    await bot.process_commands(message)

# Command: Ban a user (admin only)
@bot.command()
@is_admin()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned. Reason: {reason}")

# Command: Kick a user (admin only)
@bot.command()
@is_admin()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

# Command: Write a message to a specific channel (admin only)
@bot.command()
@is_admin()
async def write(ctx, channel_id: int, *, message: str):
    # Find the channel by ID
    channel = bot.get_channel(channel_id)
    
    if channel is None:
        await ctx.send("Channel not found. Please check the channel ID.")
        return

    # Send the message to the channel
    await channel.send(message)
    await ctx.send(f"Message has been sent to {channel.name}.")

# Error handling for commands
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must mention a user to ban them.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must mention a user to kick them.")

@write.error
async def write_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: $write CHANNEL_ID \"Your message\"")

# Start the bot
bot.run(TOKEN)
