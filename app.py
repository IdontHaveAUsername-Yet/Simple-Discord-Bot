import discord
from discord.ext import commands
import asyncio

#ADD YOUR TOKEN HERE
TOKEN = "YOUR_BOT_TOKEN_HERE"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

bad_words = [
    "idiot", "moron", "retard", "dumbass", "asshole", "arsehole", "asshat", "assclown",
    "son of a bitch", "bitch", "bastard", "motherfucker", "nigga", "nga", "nig", "n-word",
    "dickhead", "dick", "dickface", "dickwad", "cunt", "cuntface", "cuntbag", "shit",
    "shithead", "shitface", "fuck", "fucker", "fuckface", "fuckboy", "pussy", "puss",
    "pussbag", "douchebag", "douche", "douchecanoe", "arschloch", "arsch", "arschgeige",
    "arschkrampe", "arschlecker", "hurensohn", "hurenkind", "hurentochter", "hurenbengel",
    "idiot", "idiotenkind", "vollidiot", "blödmann", "wichser", "wichsbeutel", "wichsgesicht",
    "trottel", "volltrottel", "dummkopf", "depp", "volldepp", "deppert", "scheiße",
    "scheißkerl", "scheißtyp", "mistkerl", "miststück", "mistvieh", "fotze", "fotzenkind",
    "fotzengesicht", "schwanz", "schwanzlutscher", "schwanzkopf", "idiota", "imbécil",
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
            await message.author.send("Please avoid using inappropriate language.")
        except discord.Forbidden:
            await message.channel.send(f"{message.author.mention}, please do not use bad words! (I couldn't send you a DM.)")

    await bot.process_commands(message)

@bot.command()
@is_admin()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned. Reason: {reason}")

@bot.command()
@is_admin()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

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

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: $poll \"Question\" \"Option 1\" \"Option 2\" ...")

@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: $embed \"Title\" \"Description\" [color]")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must mention a user to mute them.")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must mention a user to unmute them.")

@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: $tempmute @user DURATION_IN_MINUTES [reason]")

bot.run(TOKEN)
