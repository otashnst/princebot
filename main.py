from telebot import types  # Qo‘shimcha import kerak
import telebot
import csv
import os

TOKEN = '7871677177:AAGkyPEo1uGDPZANqLE7qPT6JfuID7oOvWQ'
bot = telebot.TeleBot(TOKEN)

user_states = {}
CSV_FILE = 'participants.csv'
CODES_FILE = 'codes.txt'

# Kodlar bazasini yuklash
def load_all_codes():
    codes = set()
    if os.path.isfile(CODES_FILE):
        with open(CODES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                code = line.strip()
                if code:
                    codes.add(code)
    return codes

# Ishlatilgan kodlarni yuklash
def load_used_codes():
    used = set()
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                used.add(row['Kod'])
    return used

all_codes = load_all_codes()
used_codes = load_used_codes()

# CSV fayl yo‘q bo‘lsa, sarlavha bilan yaratamiz
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ChatID', 'Kod', 'IsmFamiliya', 'Telefon', 'Viloyat', 'Username'])

# Tugmalarni yaratish
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Kod yuborish")
    markup.row("Shou haqida", "Yordam")
    return markup

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "📢 Ishtirok etishdan oldin Instagram sahifamizga obuna bo‘ling va yangiliklarni kuzatib boring:\n"
        "👉 https://instagram.com/Prince_Muzaffarbee\n\n"
        "✅ Obuna bo‘lgan bo‘lsangiz, stiker kodingizni shu yerga yuboring:",
        reply_markup=main_menu()
    )

# Tugmalarni ishlovchi handler
@bot.message_handler(func=lambda m: m.text in ["Kod yuborish", "Shou haqida", "Yordam"])
def handle_buttons(message):
    chat_id = message.chat.id
    text = message.text

    if text == "Kod yuborish":
        start(message)  # /start funksiyasini chaqiramiz
    elif text == "Shou haqida":
        bot.send_message(chat_id, "🎭 Shou haqida:\nBu shou sizga ajoyib sovrinlar va imkoniyatlar taqdim etadi!")
    elif text == "Yordam":
        bot.send_message(chat_id, "🆘 Yordam:\nAgar savolingiz bo‘lsa, biz bilan bog‘laning: @princeshoubotadmin ")

# Asosiy muloqot
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_states:
        if text not in all_codes:
            bot.send_message(chat_id, "❌ Bunday kod bazada yo‘q. Iltimos, kodni tekshirib qaytadan kiriting.")
            return
        if text in used_codes:
            bot.send_message(chat_id, "❌ Bu kod allaqachon ishlatilgan. Iltimos, boshqa kod kiriting.")
            return

        user_states[chat_id] = {'step': 1, 'code': text}
        bot.send_message(chat_id, "✅ Kod qabul qilindi.\nEndi ismingiz va familiyangizni kiriting:")
        return

    state = user_states[chat_id]
    step = state['step']

    if step == 1:
        state['name'] = text
        state['step'] = 2
        bot.send_message(chat_id, "📞 Telefon raqamingizni kiriting:")
    elif step == 2:
        state['phone'] = text
        state['step'] = 3
        bot.send_message(chat_id, "📍 Qaysi viloyatdan ekansiz?")
    elif step == 3:
        state['region'] = text

        # CSVga yozamiz
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                chat_id,
                state['code'],
                state['name'],
                state['phone'],
                state['region'],
                message.from_user.username or ''
            ])

        used_codes.add(state['code'])  # Ishlatilgan kodlar ro'yxatiga qo'shamiz

        bot.send_message(chat_id,
            f"🎉 Rahmat, {state['name']}!\nSiz muvaffaqiyatli ro‘yxatdan o‘tdingiz!\n"
            "Yana ko‘proq mahsulot xarid qilib, imkoniyatlaringizni oshiring! 😊",
            reply_markup=main_menu()
        )

        user_states.pop(chat_id)
    else:
        bot.send_message(chat_id, "❗️ Iltimos, /start deb yozib qayta urinib ko‘ring.")

bot.polling()
