import telebot
from telebot import types
 
bot = telebot.TeleBot('TOKEN')
expr = {}
 
@bot.message_handler(commands=['start'])
def start(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.row("7", "8", "9", "del")
    kb.row("4", "5", "6", "/")
    kb.row("1", "2", "3", "*")
    kb.row("0", "+", "-", "=")
    kb.row(".", "(", ")", "conv")
    expr[msg.chat.id] = ""
    bot.send_message(msg.chat.id, "Calculator ready.", reply_markup=kb)
 
@bot.message_handler(func=lambda m: True)
def calc(m):
    cid = m.chat.id
    if cid not in expr:
        expr[cid] = ""
 
    text = m.text
 
    if text == "del":
        expr[cid] = expr[cid][:-1]
        bot.send_message(cid, expr[cid] or "0")
    elif text == "c":
        expr[cid] = ""
        bot.send_message(cid, "Cleared.")
    elif text == "=":
        try:
            result = str(eval(expr[cid]))
        except:
            result = "Error"
        bot.send_message(cid, f"{expr[cid]} = {result}")
        expr[cid] = ""
    elif text == "conv":
        try:
            val = int(eval(expr[cid]))
            msg = f"Decimal: {val}\nBinary: {bin(val)}\nOctal: {oct(val)}\nHex: {hex(val)}"
        except:
            msg = "Conversion error."
        bot.send_message(cid, msg)
        expr[cid] = ""
    else:
        expr[cid] += text
        bot.send_message(cid, expr[cid])
 
bot.polling()
