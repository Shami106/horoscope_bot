import os
import sys
import telebot
from telebot import types
from utils import get_daily_horoscope

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "The bot is running!\n\nOur bot commands:\n/start - to get started.\n/horoscope - to view your horoscope.\n/restart - to restart the bot."
    bot.reply_to(message, text)


@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
             "Aquarius", "Pisces"]
    markup.add(*[types.KeyboardButton(sign) for sign in signs])
    text = "What's your zodiac sign?"
    sent_msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(sent_msg, day_handler)


def day_handler(message):
    sign = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
    days = ["Today", "Tomorrow", "Yesterday"]
    markup.add(*[types.KeyboardButton(day) for day in days])
    text = "What day do you want to know?"
    sent_msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())


def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


@bot.message_handler(commands=['restart'])
def restart(message):
    bot.reply_to(message, "Bot is restarting...")
    python = sys.executable
    os.execl(python, python, *sys.argv)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
