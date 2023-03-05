import json
import requests
from config import currencies


class APIException (Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            if base == quote:
                raise APIException('Одна валюта введена два раза')
        except APIException as e:
            return f"Что-то пошло не так:\n{e}"

# ===========================
        #тут должна быть проверка на то, что введены корректные названия валют. Но реализовать её не получилось
        # if base not in currencies.values():
        #     raise APIException('Валюта введена неверно, или такой валюты нет в списке. \nУзнать список доступных валют: /values ')
        # elif base == quote:
        #     raise APIException('Введена одна валюта два раза')
        # ===========================

        base, quote = currencies[base], currencies[quote]
        r = requests.get(f"https://api.exchangerate.host/convert?from={base}&to={quote}&amount={amount}")
        data = json.loads(r.content)["result"]
        data = round(data, 2)
        text = f"For |{amount} {base}| You will get |{data} {quote}|"
        return text
