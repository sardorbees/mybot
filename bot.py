import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters,
)

from db import init_db, save_application
from export import export_to_excel
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Состояния
SITE_TYPE, PACKAGE, PRICE, NAME, PHONE, COMMENT = range(6)

advantages = [
    "🧩 Гибкий — адаптивность без доплат",
    "🛠 Админ — простая админ-панель",
    "🛡 Защита — от атак и вирусов",
    "🔍 Мониторинг 24/7",
    "🌐 Домен и хостинг бесплатно (6 мес)",
    "🎨 Уникальный дизайн под клиента"
]

site_types = [
    ["🌐 LANDING PAGE", "📄 Сайт-визитка"],
    ["💎 Эксклюзив", "🏫 O‘quv markaz"],
    ["🏢 Бизнес сайт", "✈ Туризм сайт"]
]

async def get_budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    budget = update.message.text
    if budget == "💬 Своя цена":
        await update.message.reply_text("✍️ Напишите свою цену в формате: например, $150")
        return CUSTOM_BUDGET
    else:
        context.user_data['budget'] = budget

        reply_keyboard = [
            ["LANDING PAGE", "SAYT VIZITKA", "ESKLYUZIV"],
            ["OQUV MARKAZ", "BIZNES UCHUN WEB SAYT", "TURISTIK KOMPANIYA UCHUN WEB SAYT"]
        ]
        await update.message.reply_text(
            "🌐 Выберите тип сайта:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        )
        return SITE_TYPE

packages = [["💼 Стандарт", "💎 Премиум"]]

price_ranges = [["💲 100$", "💲 200–300$"], ["💲 400–1000$", "💬 Своя цена"]]

init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Здравствуйте! Какой сайт вы хотите?"
    user_first_name = update.effective_user.first_name
    keyboard = [["📨 Отправить заявку", "ℹ️ О компании"]]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"👋 Привет, {user_first_name}!\n\n"
        "Добро пожаловать в наш Ali-Company Bot.\n\n"
        "🟢 Для начала работы нажми кнопку ниже или введи команду /start ещё раз.\n\n"
        "⏳ Загрузка о нас...",
        reply_markup=reply_markup
    )

    # Эмуляция загрузки
    await asyncio.sleep(2)

    await update.message.reply_text(
        "✅ Готово! Выберите действие ниже или напишите /help для подсказки."
    )

    await update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(site_types, resize_keyboard=True)
    )
    return SITE_TYPE

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [KeyboardButton("📝 Оставить заявку")],
        [KeyboardButton("📦 О нас"), KeyboardButton("📞 Поддержка")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Добро пожаловать! Выберите нужный пункт меню ниже.",
        reply_markup=reply_markup
    )
    return START

ABOUT_TEXT = (
    "🏢 <b>О нашей компании</b>\n\n"
    "🔹 Мы — команда профессиональных разработчиков сайтов.\n"
    "🔹 Делаем адаптивные, быстрые и безопасные веб-решения под ключ.\n"
    "🔹 Уникальный дизайн, простая админ-панель, бесплатный хостинг на 6 месяцев.\n"
    "🔹 Работаем с любыми нишами: образование, бизнес, туризм и т.д.\n\n"
    "Свяжитесь с нами — и ваш сайт будет лучшим! 💼"
)

async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(ABOUT_TEXT, parse_mode="HTML")

async def get_site_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["site_type"] = update.message.text
    await update.message.reply_text(
        "Выберите пакет:",
        reply_markup=ReplyKeyboardMarkup(packages, resize_keyboard=True)
    )
    return PACKAGE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Подсказки:\n\n"
        "1️⃣ Нажми '📨 Отправить заявку', чтобы оставить свою заявку\n"
        "2️⃣ Нажми 'ℹ️ О компании', чтобы узнать больше\n\n"
        "Если что-то не работает — напиши /start чтобы перезапустить бота."
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Мы создаём сайты под ключ: от идеи до запуска!\n"
        "💻 Landing Page, магазины, визитки и многое другое.\n\n"
        "Напиши нам — поможем выбрать лучший вариант!"
    )


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✍️ Пожалуйста, напишите ваше имя, номер телефона и что именно вас интересует."
    )

async def get_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["package"] = update.message.text
    await update.message.reply_text(
        "Укажите желаемую цену:",
        reply_markup=ReplyKeyboardMarkup(price_ranges, resize_keyboard=True)
    )
    return PRICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["price"] = update.message.text
    await update.message.reply_text("Введите ваше имя:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите ваш номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Комментарий или пожелания:")
    return COMMENT

async def get_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["comment"] = update.message.text
    user = update.effective_user
    username = user.username or "Нет username"

    save_application(
        context.user_data["name"],
        f"@{username}",
        context.user_data["phone"],
        context.user_data["site_type"],
        context.user_data["package"],
        context.user_data["price"],
        context.user_data["comment"]
    )

    text = (
        "📥 Новая заявка:\n\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"🔗 Username: @{username}\n"
        f"📞 Телефон: {context.user_data['phone']}\n"
        f"🌐 Сайт: {context.user_data['site_type']}\n"
        f"💼 Пакет: {context.user_data['package']}\n"
        f"💰 Цена: {context.user_data['price']}\n"
        f"💬 Комментарий: {context.user_data['comment']}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    await update.message.reply_text("✅ Ваша заявка отправлена! Мы свяжемся с вами в течение 10 минут.")
    for item in advantages:
        await update.message.reply_text(item)

    return ConversationHandler.END

async def export_applications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Только для администратора.")
        return
    path = export_to_excel()
    await context.bot.send_document(chat_id=ADMIN_ID, document=open(path, "rb"))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Заявка отменена.")
    return ConversationHandler.END

TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.Regex("^(📦 О нас)$"), about_us))
app.add_handler(CommandHandler("request", request))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SITE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_site_type)],
            PACKAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_package)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comment)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("export", export_applications))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
