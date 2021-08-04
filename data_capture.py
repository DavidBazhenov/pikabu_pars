import telebot
bot = telebot.TeleBot('1926273578:AAHl3BT5Jjkd9RtujudFXM2TS667rjo0CpY')
white_list = [['89182018959','pass123'],['89881615622','dav123'],]

@bot.message_handler(commands=['start'])
def start_message(mess):
	bot.send_message(mess.chat.id, 'бот начал работу')
@bot.message_handler(commands=['log'])
def log_mess(mess):
	numb = bot.send_message(mess.chat.id, 'введите номер телефона и пароль в формате <89992223344 password>')
	bot.register_next_step_handler(numb,check_log)
@bot.message_handler(content_types=['text'])
def check_log(message):
	global white_list
	ok = False
	try:
		number, password = message.text.lower().split(' ')
		for block in range(len(white_list)):
				if white_list[block][0] == number and white_list[block][1] == password:
					ok = True
					white_list[block][2] = (message.chat.id,)
					print(white_list)
					continue
	except:
		pass
	if ok:
		bot.send_message(message.chat.id, 'done')
	else:
		bot.send_message(message.chat.id, 'ошибка повторите процедуру   введите /log')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text.lower() == 'отправить новый документ':
		pass
bot.polling()