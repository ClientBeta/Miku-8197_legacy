import os
import google.generativeai as genai
import asyncio
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json
from memories import load_mem, save_mem

# load initial resources
load_dotenv()
DC_Token = os.getenv("DC_AUTH")
GoogleApi = os.getenv("GoogleApi")

# injects the preference file
def loadbread(source="preference.txt"):
    try:
        with open(source, "r", encoding="utf8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Wrong setting the file format. Try creating the exact `{source}`")
        return "Think what would miku hatsune think"

mikuprefernce = loadbread()

# filtered words
def filterthing(filtered="filter.json"):
    try:
        with open(filtered, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

filters = filterthing()

# Model Config
genai.configure(api_key=GoogleApi)
model = genai.GenerativeModel("gemini-2.5-flash")

intents = discord.Intents.default()
intents.message_content = True

MikuReplicated = load_mem("storage.json")

bot = commands.Bot(command_prefix="!", intents=intents)

# unload inactive people
async def unloadpeoplewhohadnotchattedawhile():
    while True:
        await asyncio.sleep(60)  # seconds timeline
        now = datetime.now(timezone.utc)
        unload_ids = []

        for userid in list(MikuReplicated.keys()):
            data = MikuReplicated.get(userid)
            if isinstance(data, dict) and "lastactive" in data:
                if now - data["lastactive"] > timedelta(minutes=4):
                    unload_ids.append(userid)

        for userid in unload_ids:
            print(f"{userid} has not chatted in a while")
            del MikuReplicated[userid]

# bot's starting point
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("CommandsLoaded")
    except Exception:
        print("Nope Fix it again bruh")

    bot.loop.create_task(unloadpeoplewhohadnotchattedawhile())

    for cog in ["slash_commands", "ReactionLib", "Randomizer"]:
        try:
            await bot.load_extension(cog)
            print(f"{cog} cog loaded.")
        except Exception as e:
            print(f"Failed to load {cog} cog: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    promt = None

    if message.reference and message.reference.resolved.author == bot.user:
        promt = message.content.strip()
    elif bot.user in message.mentions:
        promt = message.content.replace(f'<@{bot.user.id}>', '').strip()
    elif message.content.startswith("!c"):
        promt = message.content[len("!c"):].strip()

    if not promt:
        return

    theauthorithink = str(message.author.id)

    # check filters
    for word, responsetotext in filters.items():
        if word.lower() in promt.lower():
            await message.channel.send(responsetotext.replace("{userid}", theauthorithink))
            return

    now = datetime.now(timezone.utc)

    # manage session
    if theauthorithink not in MikuReplicated:
        print(f"new session for {theauthorithink}")
        history = [
            {'role': 'user', 'parts': [mikuprefernce]},
            {'role': 'model', 'parts': ["got it!"]}
        ]
        chat = model.start_chat(history=history)
        MikuReplicated[theauthorithink] = {"chat": chat, "lastactive": now}
    else:
        MikuReplicated[theauthorithink]["lastactive"] = now
        chat = MikuReplicated[theauthorithink]["chat"]

    # forward to AI
    try:
        async with message.channel.typing():
            responsetotext = await asyncio.to_thread(chat.send_message, promt)
            save_mem(MikuReplicated)
            await message.reply(responsetotext.text, mention_author=False)
    except Exception as e:
        print(f"error interaction for user {theauthorithink} code : {e}")
        await message.channel.send(f"function failure contact the owner of the bot and report the bug codename {e}")

@bot.event
async def on_disconnect():
    save_mem(MikuReplicated)
    print("adios ma homies")

# main point of the bot
async def main():
    async with bot:
        await bot.start(DC_Token)

if __name__ == "__main__":
    asyncio.run(main())
