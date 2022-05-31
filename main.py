import telebot
from config import keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду Боту в следующем формате: \n <имя валюты>' \
           '<в какую валюту перевести> <количество переводимой валюты> \n Увидить список доступных валют: /values \n' \
           'Текущий курс валют к рублю: /course'
    bot.reply_to(message, text)


# Обрабатываются сообщения, содержащие команду '/values'.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# Обрабатываются сообщения, содержащие команду '/course'.
@bot.message_handler(commands=['course'])
def course(message: telebot.types.Message):
    answer =Converter.course()
    bot.reply_to(message, answer)


# Обрабатываются все сообщения на конвертацию валют.
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Слишклом много параметров!')

        #quote, base, amount = values
        answer =Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')

    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду.\n {e}' )
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()