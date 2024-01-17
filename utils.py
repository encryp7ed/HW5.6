import requests
import json
from config import keys

# Класс исключений для отлова ошибок
class ConvertionException(Exception):
    pass

class CrypyoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозмножно конвертировать одинаковые валюты "{base}".')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{quote}".')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{base}".')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество "{amount}".')

        # Получение цены валюты с сайта
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # Печать цены запрашиваемой валюты и название валюты, в которой эта цена представлена
        total_base = json.loads(r.content)[keys[base]]

        return total_base
