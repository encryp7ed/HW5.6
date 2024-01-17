import telebot
from config import keys, TOKEN
from utils import CrypyoConverter, ConvertionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    # Инструкция по работе с ботом
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> ' \
'<в какую валюту перевести> ' \
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
    try:
        values = message.text.split(' ')

        # Проверка правильности заполнения запроса пользователем
        if len(values) != 3:
            raise ConvertionException('Передано неверное количество параметров.')

        quote, base, amount = values
        # Конвертация 1 единицы валюты
        convert = CrypyoConverter.convert(quote, base, amount)
        # Вычисление запрашиваемого количества валюты
        total_base = convert*float(amount)

    # Создаем исключение, если был введен неверный запрос
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    # Создаем исключение, если произошла ошибка на серверной части
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



# запуск бота
bot.polling()