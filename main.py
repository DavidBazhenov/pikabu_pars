import telebot
import sqlite3
import os.path

bot = telebot.TeleBot('1926273578:AAHl3BT5Jjkd9RtujudFXM2TS667rjo0CpY')
main = '753990423'
bux_list_id = ['']


@bot.message_handler(commands=['start'])
def start_message(mess):
	with sqlite3.connect('new_data.db') as db:
		cursor = db.cursor()
		query = """CREATE TABLE IF NOT EXISTS points(name INTEGER,id_from INTEGER,id_to INTEGER)"""
		cursor.execute(query)
	db.commit()

	butt = telebot.types.ReplyKeyboardMarkup(True)
	butt.row('отправить новый документ', 'войти в аккаунт')
	bot.send_message(mess.chat.id, 'секунду...', reply_markup=butt)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text.lower() == 'отправить новый документ':
		markup = telebot.types.InlineKeyboardMarkup()
		markup.add(telebot.types.InlineKeyboardButton(text='название проекта', callback_data=1))
		markup.add(telebot.types.InlineKeyboardButton(text='название проекта', callback_data=2))
		markup.add(telebot.types.InlineKeyboardButton(text='название проекта', callback_data=3))
		bot.send_message(message.chat.id, text="выберите город", reply_markup=markup)
	elif message.text.lower() == 'войти в аккаунт':
		bot.send_message(message.chat.id, text="введите /log + номер телефона в формате ( 89992223344 )")




# отправить новый документ
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	bot.answer_callback_query(callback_query_id=call.id, text='...')
	answer = ''
	if call.data == '1':
		answer = 'отлично'
	elif call.data == '2':
		answer = 'отлично'
	elif call.data == '3':
		answer = 'отлично'
	bot.send_message(call.message.chat.id, answer)
# log in
@bot.message_handler(commands=['/log'])
def decode(message):
	phone = message.text
	bot.send_message(mess.chat.id, f"секунду...  Отлично {phone}")



bot.polling()
