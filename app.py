import telebot
import requests
import json


TOKEN = '6932268025:AAGzSbrGNnEgQWB6THKQXI9emE488Uxu-p8'


bot = telebot.TeleBot(TOKEN)


keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD'
}


class ConvertionException(Exception):
    pass


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    # инструкция по работе с ботом
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты>' \
'<в какую валюту перевести>' \
'<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) > 3:
        raise ConvertionException('Слишком много параметров.')

    quote, base, amount = values

    if quote == base:
        raise ConvertionException(f'Невозмножно конвертировать одинаковые валюты {base}.')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {quote}')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {base}')

    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Не удалось обработать количество {amount}')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
    # Печать цены запрашиваемой валюты и название валюты, в которой эта цена представлена
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)



# запуск бота
bot.polling()