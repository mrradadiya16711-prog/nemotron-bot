import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hey! I'm powered by NVIDIA Nemotron 3 Super. Ask me anything!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = requests.post(
            "https://nvidia.com",
            headers={
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "nvidia/nemotron-3-22b-chat-hf",
                "messages": [{"role": "user", "content": user_message}],
                "temperature": 0.7,
                "max_tokens": 1024
            },
            timeout=30
        )

        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            ai_reply = data["choices"][0]["message"]["content"]
        else:
            ai_reply = f"Sorry, I got an unexpected response: {data}"
    except Exception as e:
        ai_reply = f"Sorry, I encountered an error: {str(e)}"

    await update.message.reply_text(ai_reply)

async def main():
    if not TELEGRAM_TOKEN or not NVIDIA_API_KEY:
        print("❌ Error: Missing Environment Variables!")
        return

    # Add custom network timeouts
    custom_request = HTTPXRequest(
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0
    )

    # Use a secure alternative proxy URL to route past the Hugging Face firewall
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .base_url("https://proxy.tl")
        .request(custom_request)
        .build()
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    print("🚀 Nemotron 3 Super Bot is starting...")
    
    async with app:
        await app.initialize()
        await app.start()
        print("🚀 Nemotron 3 Super Bot is running live!")
        await app.updater.start_polling(connect_timeout=60.0)
        
        while True:
            await asyncio.sleep(3600)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bot stopped manually.")
