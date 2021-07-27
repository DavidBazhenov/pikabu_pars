import telebot
import requests
from bs4 import BeautifulSoup as BS
import fake_useragent

url = 'https://pikabu.ru/tag/%D0%AE%D0%BC%D0%BE%D1%80?q=%D0%BC%D0%B5%D0%BC&et=%D0%9F%D0%BE%D0%BC%D0%BE%D1%89%D1%8C&st=100&page='
bot = telebot.TeleBot('1758823185:AAGae5HNmOpUJRmH_EDE3pZx6jpvWVR2tbc')
count = 0
user = fake_useragent.UserAgent().random
header = {'user-agent': user}
page_count = 0
list_img = []
list_title = []
ban = ['мем', 'мемы', 'Мем', 'Мемы', 'новый мем', 'Новый мем']


@bot.message_handler(commands=['start'])
def start_message(mess):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('новый пост')
    bot.send_message(mess.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global count, page_count, list_img, list_title, ban
    k = 0
    if message.text.lower() == 'новый пост':
        # обновление data
        if count == 0:
            file = open(f'data_{message.from_user.id}', 'r')
            page_count, count = file.readline().split('_')
            file.close()
            page_count = int(page_count)
            count = int(count)
            responce = requests.get(url + str(page_count), headers=header).text
            soup = BS(responce, 'lxml')
            post_big_block = soup.find('div', class_='stories-feed__container')
            list_img = post_big_block.find_all('div', class_='story__content-inner')
            list_title = post_big_block.find_all('h2', class_='story__title')
        else:
            count += 1
            file = open(f'data_{message.from_user.id}', 'w')
            file.write(f'{page_count}_{count}')
            file.close()

        if len(list_img) < count:
            page_count += 1
            responce = requests.get(url + str(page_count), headers=header).text
            soup = BS(responce, 'lxml')
            post_big_block = soup.find('div', class_='stories-feed__container')
            list_img = post_big_block.find_all('div', class_='story__content-inner')
            list_title = post_big_block.find_all('h2', class_='story__title')

            count = 1
        if len(list_img) != 0:
            if list_title[count - 1].find('a').text not in ban:
                bot.send_message(message.from_user.id, list_title[count - 1].find('a').text)
            for blok in list_img[count - 1].find_all('div', ['story-block story-block_type_text',
                                                             'story-block story-block_type_image',
                                                             'story-block story-block_type_video',
                                                             'story-block story-block_type_image story-block_padding_left',
                                                             'story-block story-block_type_image story-block_padding_right']):
                # print(blok)
                list_txt = blok.find_all('p')
                list_photo = blok.find_all('img')
                list_video = blok.find_all('div', class_='player')
                # текст

                if len(list_txt) != 0:
                    for TXT in list_txt:
                        try:
                            k += 1
                            bot.send_message(message.from_user.id, TXT.text)
                        except:
                            continue
                # ВИДЕО
                elif len(list_video) != 0:

                    for mov in list_video:
                        if 'pikabu' in mov.get('data-source'):
                            video_url = mov.get('data-webm')

                            viv = requests.get(video_url).content
                            bot.send_video(message.chat.id, viv)
                        else:
                            bot.send_message(message.from_user.id, mov.get('data-source'))
                # ФОТО

                elif len(list_photo) != 0:
                    for IMG in list_photo:
                        img_url = IMG.get('data-large-image')
                        dow_img = requests.get(img_url).content
                        bot.send_photo(message.from_user.id, dow_img)


    else:
        bot.send_message(message.from_user.id, 'бот находится в разработкеБ могут присутствовать баги и недоработки')


bot.polling(none_stop=True)
