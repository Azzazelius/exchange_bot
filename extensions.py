import json
import requests
from config import currencies


# Класс наследует встроенный класс Exception. Дополнительная логика не требуется, поэтому класс пустой.
# Используется для вывода исключений
class APIException (Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            if base == quote:
                raise APIException('Одна валюта введена два раза')
        except APIException as e:
            return f"'Одна валюта введена два раза'\n{e}"

        try:
            if base not in currencies.values() or quote not in currencies.values():
                raise APIException('Валюта введена неверно или такой валюты нет в списке.')

            # обращение в exchangerate за курсом конвертации
            r = requests.get(f"https://api.exchangerate.host/convert?from={base}&to={quote}&amount={amount}")
            r.raise_for_status()  # Проверка на успешный статус ответа
        except requests.exceptions.RequestException:
            raise APIException('Ошибка при выполнении запроса')

        data = json.loads(r.content)["result"]
        data = round(data, 2)
        text = f"For |{amount} {base}| You will get |{data} {quote}|"
        return text
