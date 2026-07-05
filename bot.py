import os                                                                                                │
│             import requests                                                                                          │
│             from telegram import Update                                                                              │
│             from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes       │
│                                                                                                                      │
│             TELEGRAM_TOKEN=***                                                                                       │
│             NVIDIA_API_KEY=***                                                                                       │
│                                                                                                                      │
│             async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):                                     │
│                 await update.message.reply_text("🤖 Hey! I'm powered by NVIDIA Nemotron 3 Super. Ask me anything!")  │
│                                                                                                                      │
│             async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):                                      │
│                 user_message = update.message.text                                                                   │
│                                                                                                                      │
│                 try:                                                                                                 │
│                     response = requests.post(                                                                        │
│                         "https://integrate.api.nvidia.com/v1/chat/completions",                                      │
│                         headers={                                                                                    │
│                             "Authorization": f"Bearer {NVIDIA_API_KEY}",                                             │
│                             "Content-Type": "application/json"                                                       │
│                         },                                                                                           │
│                         json={                                                                                       │
│                             "model": "nvidia/nemotron-3-22b-chat-hf",  # Nemotron 3 Super!                           │
│                             "messages": [{"role": "user", "content": user_message}],                                 │
│                             "temperature": 0.7,                                                                      │
│                             "max_tokens": 1024                                                                       │
│                         },                                                                                           │
│                         timeout=30                                                                                   │
│                     )                                                                                                │
│                                                                                                                      │
│                     data = response.json()                                                                           │
│                     if "choices" in data and len(data["choices"]) > 0:                                               │
│                         ai_reply = data["choices"][0]["message"]["content"]                                          │
│                     else:                                                                                            │
│                         ai_reply = f"Sorry, I got an unexpected response: {data}"                                    │
│                 except Exception as e:                                                                               │
│                     ai_reply = f"Sorry, I encountered an error: {str(e)}"                                            │
│                                                                                                                      │
│                 await update.message.reply_text(ai_reply)                                                            │
│                                                                                                                      │
│             if __name__ == "__main__":                                                                               │
│                 app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()                                             │
│                 app.add_handler(CommandHandler("start", start))                                                      │
│                 app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))                               │
│                 print("🚀 Nemotron 3 Super Bot is running...")                                                       │
│                 app.run_polling()                                                                                    │
│             ```                             