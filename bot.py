from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os, time
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return

    msg = update.message
    text = msg.text or ""
    filename = f"{int(time.time())}.md"
    post_path = f"blog/posts/{filename}"

    image_url = None
    if msg.photo:
        file = await context.bot.get_file(msg.photo[-1].file_id)
        ext = file.file_path.split('.')[-1]
        img_name = f"{filename}.{ext}"
        img_path = f"static/img/{img_name}"
        await file.download_to_drive(img_path)
        image_url = f"/static/img/{img_name}"

    with open(post_path, "w") as f:
        if image_url:
            f.write(f"![img]({image_url})\n\n")
        f.write(text)

    print(f"✅ Post salvato: {post_path}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))
app.run_polling()
