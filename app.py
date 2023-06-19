import telebot
from config import TOKEN, currencies
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

# Функция для бота, обёрнута в декоратор из telebot. Команды выводят инструкцию
@bot.message_handler(commands=["start", "help"])
def show_instruction(message):
    bot.send_message(message.chat.id, f"Введите запрос в формате: "
                                      f"\n<валюта 1> <валюта 2> <количество первой валюты>."
                                      f"\n"
                                      f"\nСписок доступных валют: /values")


# Функция для бота. Выводит список доступных валют
@bot.message_handler(commands=["values"])
def show_currencies(message):
    text = "Доступные валюты:"
    for cur in currencies.keys():
        text = "\n".join((text, cur))
    bot.send_message(message.chat.id, text)


# Функция бота. Запрашивает информацию для ввода
@bot.message_handler(content_types=['text'])
def converter(message):
    in_between_list = message.text.lower().split(' ')
    try:
        # проверка, что введено 3 параметра
        if len(in_between_list) != 3:
            raise APIException('Неверное количество параметров!')
    except APIException as e:
        bot.send_message(message.chat.id, f"Что-то пошло не так:\n{e}")
    else:
        base, quote, amount = in_between_list
        # Если всё правильно 3 переменные отправляются в класс Converter. Бот выводит сообщение с результатом
        # выполнения метода get_price
        bot.send_message(message.chat.id, Converter.get_price(base, quote, amount))


# строки для улучшения читабельности консоли.
print("=============================================================================")
print("============================Bot has been launched============================")
print("=============================================================================")

bot.polling()

