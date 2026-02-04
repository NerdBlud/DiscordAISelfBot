# DiscordAISelfBot

This is a personal Discord selfbot project I built to experiment with making an AI that actually feels more human in chat, not like a boring assistant bot. Instead of just replying, it keeps lightweight memory and tracks how it “feels” about different users so conversations can evolve over time.

## What This Bot Tries to Do

Most Discord bots feel robotic because they forget everything and talk too formally. This project tries to fix that by focusing on:

* Talking like a real person (lowercase, slang, short replies)
* Remembering recent conversations
* Keeping simple emotional context about users
* Avoiding obvious “AI assistant” behavior

It’s designed to blend in, not stand out as a bot.

## Core Features

### Human-Style Messaging

The bot intentionally avoids proper grammar and formal tone. It uses modern slang and short casual responses so it doesn’t sound like a help desk or customer support bot.

### Conversation Memory

It keeps a rolling memory of the last 100 messages per context so replies reference recent stuff instead of feeling disconnected or random.

### Persistent Feelings System

Each user has a simple emotional profile stored in a local JSON file. This lets the bot:

* Act friendlier to people it’s talked to a lot
* Get more dry or dismissive with spammy users
* Slightly change its vibe depending on past interactions

This makes the bot feel more consistent over time instead of resetting every run.

## Tech Stack

| Part            | What’s Used                 |
| --------------- | --------------------------- |
| Language        | Python 3.10+                |
| AI Model        | Groq (Llama-3.1-8b-instant) |
| Discord Lib     | discord.py-self             |
| Storage         | Local JSON files            |
| Typical Latency | Usually under 1 second      |

## The Feelings System (How It Actually Works)

The “feelings” engine is just a lightweight scoring and state system. It’s not real emotions, it’s just logic that helps keep behavior consistent.

Each user can fall into rough states like:

* Friend: Regular positive interaction
* Annoyed: Repeated spam, boring messages, or low-effort stuff
* High Interest: Lots of engagement and back-and-forth
* Neutral: Default state

These are stored in feelings.json and loaded on startup so the bot doesn’t forget people.

The system prompt uses this data to slightly change tone and response style per user.

## Installation

### Install Dependencies

```bash
pip install discord.py-self groq
```

### Configure Credentials

Open bot.py and set:

* DISCORD_TOKEN — Your Discord account token
* GROQ_API_KEY — Your Groq API key
* TARGET_CHANNEL_ID — The channel where the bot is allowed to talk

### Run

```bash
python bot.py
```

## Important Notes and Warnings

* Selfbots violate Discord TOS. Use this at your own risk.
* Rate limiting matters. The default cooldown is 1.5 seconds. Going lower makes bans way more likely.
* Keep tokens private. Never push real tokens to GitHub.
* feelings.json contains user IDs. Treat it as private data.

## Why This Exists

This project is mostly for learning and experimentation:

* Prompt engineering
* Memory systems
* Making AI feel less robotic
* Testing how personality changes affect conversations