import telebot
@bot.message_handler(commands=['start'])
def start_message(mess):
	keyboard = telebot.types.ReplyKeyboardMarkup(True)
	keyboard.row('отправить данные')
	bot.send_message(mess.chat.id, 'секунду...', reply_markup=keyboard)