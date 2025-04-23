import telebot
from telebot import types
 
bot = telebot.TeleBot('TOKEN')
 
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🪨 Rock', '📄 Paper', '✂️ Scissors')
    bot.send_message(message.chat.id, "Choose one:", reply_markup=markup)
 
@bot.message_handler(func=lambda m: True)
def play(message):
    if message.text == '🪨 Rock':
        bot.send_message(message.chat.id, "I choose 📄 Paper! I win! 😎")
    if message.text == '📄 Paper':
        bot.send_message(message.chat.id, "I choose ✂️ Scissors! I win! 😎")
    if message.text == '✂️ Scissors':
        bot.send_message(message.chat.id, "I choose 🪨 Rock! I win! 😎")
 
bot.polling()
