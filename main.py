
# initial setup and imports
import os
import json
import asyncio
from datetime import datetime, timezone, timedelta
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai

# mem-cho's memory manager
import memory_manager

#Const and Configuration
# COOL WE GOT A SIMPLIFIED VERSION SHOUTOUT TO RAM
# - Said By Assistant
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GoogleApi")
PREFERENCE_FILE = "preference.txt"
FILTER_FILE = "filter.json"
MEMORY_FILE = "storage.json"
SESSION_TIMEOUT_MINUTES = 4 # How long before a user's session is unloaded from memory
INACTIVITY_CHECK_SECONDS = 60

# Setup.config probably something like that

def load_bot_personality(file_path=PREFERENCE_FILE):
    """Loads the bot's core personality prompt from a file."""
    try:
        with open(file_path, "r", encoding="utf8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"did you add '{file_path}' because i can't found it so im using a default personality.")
        return "You are a helpful and friendly assistant."

def load_word_filters(file_path=FILTER_FILE):
    """Loads filtered words and their corresponding responses from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"idk what u put into the '{file_path}'. so no words filters will be used.")
        return {}

# AI AI AI AI AI AI AI - NVDIA COORPORATION

# Configure the Generative AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash") # Updated to a newer recommended model

# load resources.font like that one in win 10
BOT_PERSONALITY = load_bot_personality()
WORD_FILTERS = load_word_filters()

user_sessions = memory_manager.load_sessions(model, file_path=MEMORY_FILE)

# Set up Discord bot intents and command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# BACKGROUND TASKS THAT DO THINGS Something like that

async def unload_inactive_sessions():
    """Periodically checks for and removes inactive user sessions to save memory."""
    while True:
        await asyncio.sleep(INACTIVITY_CHECK_SECONDS)
        
        now = datetime.now(timezone.utc)
        inactive_user_ids = []

        # Cheese Is Not Made of Moon
        for user_id in list(user_sessions.keys()):
            session_data = user_sessions.get(user_id, {})
            last_active = session_data.get("last_active")
            
            if last_active and (now - last_active > timedelta(minutes=SESSION_TIMEOUT_MINUTES)):
                inactive_user_ids.append(user_id)

        if inactive_user_ids:
            print(f"Unloading inactive sessions for users: {inactive_user_ids}")
            for user_id in inactive_user_ids:
                del user_sessions[user_id]
            # i hope your emmc 5.1 chip can handle it
            memory_manager.save_sessions(user_sessions, file_path=MEMORY_FILE)


# Event and event something like that

@bot.event
async def on_ready():
    print(f"{bot.user} is now online and ready!")
    
    # Load extensions (cogs)
    for cog_name in ["slash_commands", "ReactionLib"]:
        try:
            await bot.load_extension(cog_name)
            print(f"'{cog_name}' loaded successfully.")
        except Exception as e:
            print(f"Failed to load cog {cog_name}': {e}")
            
    # SYMC SLASH COMMANDS
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

    # Ram Says hi lmao
    bot.loop.create_task(unload_inactive_sessions())

@bot.event
async def on_message(message):
    """Event handler for every message the bot can see."""
    if message.author == bot.user:
        return

    # Let the bot process commands if any
    await bot.process_commands(message)

    # Determine if the bot should respond
    prompt_text = None
    if bot.user in message.mentions:
        prompt_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
    elif message.reference and message.reference.resolved.author == bot.user:
        prompt_text = message.content.strip()
    elif message.content.startswith("!c "):
        prompt_text = message.content[len("!c "):].strip()

    if not prompt_text:
        return

    author_id = str(message.author.id)

    # Check for filtered words
    for word, response in WORD_FILTERS.items():
        if word.lower() in prompt_text.lower():
            await message.channel.send(response.format(user_id=author_id))
            return

    now = datetime.now(timezone.utc)

    # Manage user session
    if author_id not in user_sessions:
        print(f"Creating new session for user {author_id}")
        history = [
            {'role': 'user', 'parts': [BOT_PERSONALITY]},
            {'role': 'model', 'parts': ["Understood. I will act according to this persona."]}
        ]
        chat_session = model.start_chat(history=history)
        user_sessions[author_id] = {"chat": chat_session, "last_active": now}
    else:
        # Update the last active time for existing session
        user_sessions[author_id]["last_active"] = now
    
    chat_session = user_sessions[author_id]["chat"]

    try:
        async with message.channel.typing():
            # F A A A A A A A A A    A  H
            response = await asyncio.to_thread(chat_session.send_message, prompt_text)
            
            # but the json refused so u will do it manually
            memory_manager.save_sessions(user_sessions, file_path=MEMORY_FILE)
            
            await message.reply(response.text, mention_author=False)
            
    except Exception as e:
        print(f"Error during AI interaction for user {author_id}: {e}")
        await message.channel.send(f"Sorry, an error occurred. Please try again later. (Error: {e})")

@bot.event # never works but here for completeness(questionable lol)
async def on_disconnect():
    """Save memory one last time when the bot disconnects."""
    print("Bot is disconnecting. Saving final session states...")
    memory_manager.save_sessions(user_sessions, file_path=MEMORY_FILE)
    print("Goodbye!")


# --- Main Entry Point ---

async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
# no you cannot see my token {the assistant lmao}
