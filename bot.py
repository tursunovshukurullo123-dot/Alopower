import telebot
from telebot import types

TOKEN = "8913508666:AAFUSgBZuB6aoKVfhBSSJfsDxAIQuMNLVKU"
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasi (vaqtincha xotirada turadi)
zaryadniklar = {}  # {nomi: {"oddiy": narx, "doimiy": narx, "soni": soni}}
mijozlar = set()   
savdolar = []      

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Zaryadnik qo'shish", "📋 Zaryadniklar ro'yxati")
    markup.add("👥 Doimiy mijozlar", "📊 Hisobot")
    bot.send_message(
        user_id, 
        "Assalomu alaykum! Zaryadniklar savdosi va ombor boshqaruv botiga xush kelibsiz. Kerakli bo'limni tanlang:", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id

    if text == "📦 Zaryadnik qo'shish":
        bot.send_message(
            chat_id, 
            "Yangi zaryadnik qo'shish uchun ma'lumotni quyidagi formatda yuboring:\n\n`Nomi | Oddiy narx | Doimiy narx | Soni`\n\n*Misol:* `Samsung 25W | 50000 | 40000 | 15`", 
            parse_mode="Markdown"
        )
    elif text == "📋 Zaryadniklar ro'yxati":
        if not zaryadniklar:
            bot.send_message(chat_id, "Hozircha zaryadniklar qo'shilmagan.")
        else:
            javob = "📦 **Zaryadniklar bazasi:**\n\n"
            for nomi, info in zaryadniklar.items():
                javob += f"• *{nomi}*\n  ▫️ Oddiy narx: {info['oddiy']} so'm\n  ▫️ Doimiy mijozga: {info['doimiy']} so'm\n  ▫️ Qoldiq: {info['soni']} dona\n\n"
            bot.send_message(chat_id, javob, parse_mode="Markdown")
    elif "|" in text:
        try:
            parts = [p.strip() for p in text.split("|")]
            nomi, oddiy, doimiy, soni = parts[0], int(parts[1]), int(parts[2]), int(parts[3])
            zaryadniklar[nomi] = {"oddiy": oddiy, "doimiy": doimiy, "soni": soni}
            bot.send_message(chat_id, f"✅ Muvaffaqiyatli qo'shildi:\n*{nomi}* — {soni} dona", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(chat_id, "❌ Xatolik! Formatni to'g'ri kiriting:\n`Nomi | Oddiy narx | Doimiy narx | Soni`", parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "Tushunarsiz buyruq. Tugmalardan foydalaning.")

if __name__ == '__main__':
    bot.infinity_polling()
