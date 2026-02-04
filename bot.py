import discord
from discord.ext import commands
from groq import Groq
import asyncio
import random
import json
import os
from collections import deque

DISCORD_TOKEN = 'USER_TOKEN_HERE'
GROQ_API_KEY  = 'GROQ_API_KEY_HERE'
TARGET_CHANNEL_ID = CHANNEL_ID_HERE 
COOLDOWN_SECONDS = 1.5 # Adjustable, minimum: 1 maximum: 5 
MAX_HISTORY = 100 # Adjustable, 100 is recommended
FEELINGS_FILE = 'feelings.json' # do not touch

client = Groq(api_key=GROQ_API_KEY)

DISCORD_USER_PERSONA = """
you’re just a regular discord homie.
- type mostly lowercase, skip formal punctuation.
- keep replies short (3-8 words).
- be sarcastic or hype. you can develop real feelings for people (crush, annoyance, friendship).
"""

bot = commands.Bot(command_prefix='>', self_bot=True)
last_reply_time = {}
message_history = {}

def load_feelings():
    if os.path.exists(FEELINGS_FILE):
        with open(FEELINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_feeling(user_id, feeling):
    data = load_feelings()
    data[str(user_id)] = feeling
    with open(FEELINGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'--- [EMOTIONAL GROQ BOT ONLINE] ---')
    print(f'Feelings being saved to: {FEELINGS_FILE}')

@bot.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID or message.author.id == bot.user.id or message.author.bot:
        return

    current_time = asyncio.get_event_loop().time()
    if message.author.id in last_reply_time:
        if current_time - last_reply_time[message.author.id] < COOLDOWN_SECONDS:
            return 

    user_feelings = load_feelings()
    current_feeling = user_feelings.get(str(message.author.id), "neutral/stranger")

    if message.channel.id not in message_history:
        message_history[message.channel.id] = deque(maxlen=MAX_HISTORY)

    message_history[message.channel.id].append({"role": "user", "content": message.content})

    try:
        async with message.channel.typing():
            await asyncio.sleep(random.uniform(0.4, 0.9))
            
            dynamic_persona = DISCORD_USER_PERSONA + f"\nYour current feeling for this user is: {current_feeling}."
            
            messages_payload = [{"role": "system", "content": dynamic_persona}]
            messages_payload.extend(list(message_history[message.channel.id]))

            chat_completion = client.chat.completions.create(
                messages=messages_payload,
                model="llama-3.1-8b-instant",
                temperature=1.2,
                max_tokens=60
            )
            
            raw_text = chat_completion.choices[0].message.content
            
            if raw_text:
                final_text = raw_text.strip().lower()
                new_feeling = current_feeling
                
                if "[feeling:" in final_text:
                    parts = final_text.split("[feeling:")
                    final_text = parts[0].strip().replace('"', '')
                    new_feeling = parts[1].replace("]", "").strip()
                    save_feeling(message.author.id, new_feeling) 

                last_reply_time[message.author.id] = current_time
                message_history[message.channel.id].append({"role": "assistant", "content": final_text})
                
                await message.reply(final_text)
                print(f"To {message.author.name}: {final_text} | Feeling: {new_feeling}")

    except Exception as e:
        print(f"Groq Error: {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)