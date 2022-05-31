import json
import requests
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты: {base}!')

        try:
            quote_key = keys[quote]
        except KeyError:
            raise APIException(f'Неудалось обработать валюту: {quote}!')

        try:
            base_key = keys[base]
        except KeyError:
            raise APIException(f'Неудалось обработать валюту: {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неудалось обработать количество: {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}')
        prise = json.loads(r.content)[keys[quote]]
        total_prise = round(prise * amount, 2)
        amount = round(amount, 2)
        answer = f'Цена {amount} {base} в {quote} - {total_prise}'

        return answer


    @staticmethod
    def course():
        usd = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=RUB')
        eur = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym=EUR&tsyms=RUB')
        usd = json.loads(usd.content)[keys['рубль']]
        eur = json.loads(eur.content)[keys['рубль']]
        answer = f'Текущий курс валют к рублю: \n' \
                 f'Доллар \t- {usd}\n' \
                 f'Евро \t  - {eur}\n'
        return answer


