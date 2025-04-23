translator = Translator()
user_data = {}
 
langs = {'en': '🇬🇧 English', 'es': '🇪🇸 Spanish', 'it': '🇮🇹 Italian'}
 
@bot.message_handler(func=lambda m: True)
def ask_source(message):
    user_data[message.chat.id] = {'text': message.text}
    markup = types.InlineKeyboardMarkup()
    for code, name in langs.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"from_{code}"))
    bot.send_message(message.chat.id, "From which language?", reply_markup=markup)
 
@bot.callback_query_handler(func=lambda call: call.data.startswith("from_"))
def ask_target(call):
    code = call.data.split("_")[1]
    user_data[call.message.chat.id]['src'] = code
    markup = types.InlineKeyboardMarkup()
    for code, name in langs.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"to_{code}"))
    bot.edit_message_text("To which language?", call.message.chat.id, call.message.message_id, reply_markup=markup)
 
@bot.callback_query_handler(func=lambda call: call.data.startswith("to_"))
def translate(call):
    code = call.data.split("_")[1]
    chat_id = call.message.chat.id
    text = user_data[chat_id]['text']
    src = user_data[chat_id]['src']
    translated = translator.translate(text, src=src, dest=code)
    bot.send_message(chat_id, translated.text)
 
bot.polling()
