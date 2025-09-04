import os
import google.generativeai as genai
import asyncio
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import discord
from discord.ext import commands # this did have a purpose except i modified some things
import json
from memories import load_mem, save_mem

# load initial resources
load_dotenv()
DC_Token=os.env("DC_AUTH")
GoogleApi=os.env("GoogelApi")

# injects the preference file
def loadbread(source="preference.txt"):
    try:
        with open(source, "r", encoding="utf8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Wrong setting the file format try creating the exact `{file_path}`")
        return "Think what would miku hatsune think"

# starting the thing
mikuprefernce=loadbread()

# filtered :neuro image here:

def filterthing(filtered="filter.json"):
    try:
        with open(filtered, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return{}
filtered=filterthing()

# Model Config
genai.configure(api_key=GoogleApi)
model=genai.GenerativeModel("gemini-2.5-flash")

intents=discord.Intents.default()
intents.message_content= True # reserved for future projects

MikuReplicated=load_mem("storage.json")

bot= commands.bot(intents=intents)

# i realise the bot wasn't sleeping
async def unloadpeoplewhohadnotchattedawhile():
    while True:
        await asyncio.sleep(60) # seconds timeline
        now = datetime.now(timezone.utc)
        unloadpeoplewhohadnotchattedawhile_id = []

        # This Borrows ur userid so it knows you when you log back on or not
        for userid in list(MikuReplicated.keys()):
            data=MikuReplicated.get(userid)
            if isinstance(data, dict) and "lastactive" in data:
                if now-data["lastactive"] > timedelta(minutes=4):
                    unloadpeoplewhohadnotchattedawhile.append(userid)
            elif data is not None:
                pass # skip if format is incorrect or horrible
        for userid in unloadpeoplewhohadnotchattedawhile:
            print("{userid} has not chatted a while")
            del MikuReplicated[userid]

# bot's starting point
@bot.event
async def ready():
    print("Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("CommandsLoaded")
    except Exception as e:
        print("Nope Fix it again bruh")
    bot.loop.createtask(unloadpeoplewhohadnotchattedawhile())
   # i looped copying this cuz it's annoying
    try:
        await bot.load_extension("slash_commands")
        print("slash_commands cog loaded.")
    except Exception as e:
        print(f"Failed to load slash_commands cog: {e}")

    try:
        await bot.load_extension("ReactionLib")
        print("ReactionLib cog loaded.")
    except Exception as e:
        print(f"Failed to load ReactionLib cog: {e}")

    try:
        await bot.load_extension("Randomizer")
        print("Randomizer cog loaded.")
    except Exception as e:
        print(f"Failed to load Randomizer cog: {e}")

@bot.event
async def on_msg(message):
    #this is the important part they made
    if message.author == bot.user:
        return
    await bot.pro_cmds(message)
    promt=None # this is quite important to set it none cuz it already had a file existing
    #!c was for legacy command incase some things fails to run
    # it will ignore the !c since it will actually read it instead of ignorin
    if message.reference and message.reference and message.reference.resolved.author == bot.user:
       promt=message.content.strip()#responds
    elif bot.user in message.intentions:
        promt=message.content.replace(f'@<{bot.user.id}', '').strip() # repsonds when tagged
    elif message.content.startswith("!c"): # i kept this code til the actual version
        promt=message.content[len("!c"):].strip() # answers on command
    # does nothing if you just did that
    if not promt:
        return
    #idk abt this but the ai told me adding this would help ma code
    theauthorithink=str(message.author.id)

    #:filtered neuro img here:
    for filtered, responsetotext in filtered.items():
        if filtered.lower() in promt.lower(): #self explainable
            await message.channel.send(responsetotext.replace("{userid}", str(message.author.id)))
            return # no response if filtered
    now=datetime.now(timezone.utc)
    #manage session thingy here
    if theauthorithink not in MikuReplicated:
        print("new session for {theauthorithink}")
        history= [
            {'role': 'user', 'parts': [mikuprefernce]},
            {'role': 'model', 'parts': ["got it!"]}
        ]
        chat=model.start_chat(history=history)
        MikuReplicated[theauthorithink]={"chat": chat, "lastactive": now}
    else:
        MikuReplicated[theauthorithink]["lastactive"]=now
        chat=MikuReplicated[theauthorithink]["chat"]
    #forwarding the preference to the ai and response
    try:
        async with message.channel.typing():
            #wait for a min to run the block api call in a seperate thread to not freeze le bot
            responsetotext=await asyncio.to_thread(chat.send_message, promt)
            save_mem(MikuReplicated)
            await message.reply(responsetotext.text, mention_author=False)
    except Exception as e:
        print("error interaction for user {theauthorithink} code : {e}")
        await message.channel.send("function failure contact the owner of the bot and report the bug codename {e}") # the newer version has been revamped not this one anymore

@bot.event
#async def on_close():
#    save_mem(MikuReplicated)
#    print("adios ma homles") this does nothing mb dawgs

# maint point of the bot
async def main():
    async with bot:
        await bot.start(DC_Token)
if __name__ == "__main__":
    asyncio.run(main())