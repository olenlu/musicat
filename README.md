# Telegram bot for downloading audio from YouTube vidios 

# 🎵 Musicat — Telegram Bot for Downloading YouTube Audio

**Musicat** is a simple and convenient Telegram bot that allows you to download audio from YouTube based on a search query.

It's perfect when you quickly need a song, live performance, interview, podcast, or anything else — with no extra hassle.

---

## ⚙️ How It Works

1. **Send a search query** — song title, artist name, or keywords  
   _Example: `prodigy smack my bitch up`_

2. **Get top 5 results** — the bot will respond with the best matches, each with a title and a YouTube link.

3. **Choose a result** — send `/1`, `/2`, etc., to pick the audio you want.

4. **Receive the audio** — the bot will download and send the audio file back to you.

---

## 🔧 Setup

1. After cloning the repository:

2. Create a `.env` file in the project's root directory

3. Add your bot token in `.env` in the following format:
   BOT_TOKEN=your_token_here

---

## 🐳 Build & Run with Docker

1. Navigate to the root directory of the project:

2. Build the Docker image:
    docker build -t telegram-bot .
3. Run the container:
    docker run -d telegram-bot

