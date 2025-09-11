import json
import math
import re
from datetime import datetime
from typing import Any, Dict, List

from src.utils import cashback_log, investment_log, phone_number_log, search_individuals_log, simple_search_1_log


def increased_cashback_categories(data: list[dict], date_user: str) -> str:
    """Анализ выгодных категорий повышенного кэшбэка"""

    cashback_log.info("Запуск функции анализа кэшбэка")

    filter_data = []
    sort_categories = {}

    for data_dict in data:
        if datetime.strptime(data_dict["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y") == date_user:

            if data_dict["Кэшбэк"] is not None or data_dict["Бонусы (включая кэшбэк)"] > 0:
                filter_data.append(data_dict)
    cashback_log.info("Поиск выбранного периода")

    for data_dict_2 in filter_data:
        sort_categories[data_dict_2["Категория"]] = data_dict_2.get("Бонусы (включая кэшбэк)")

        if data_dict_2["Кэшбэк"] is not None:
            sort_categories[data_dict_2["Категория"]] += data_dict_2.get("Кэшбэк")
    cashback_log.info("Поиск выгоды")

    result = dict(sorted(sort_categories.items(), key=lambda item: item[1], reverse=True))

    return json.dumps(result, ensure_ascii=False, indent=4)


# if __name__ == '__main__':
#     """Для выгодных категорий с выбором пользователем параметров"""
#
#     month = input('Введите месяц -> ')
#     year = input('Введите год -> ')
#     date_full = month + '.' + year
#
#     func_date = date_analiz(date_full)
#     func_data = reading_excel_file(file)
#     print(increased_cashback_categories(func_data, func_date))


def investment_bank(date: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """Инвесткопилка"""

    investment_log.info("Запуск функции инвесткопилки")
    result = []
    investment_log.info("Фильтрация трат от пополнений")
    for transaction in transactions:
        if datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y") == date:
            if transaction["Сумма операции"] < 0:

                amount = transaction["Сумма операции"] * -1

                rounded = math.ceil(amount / limit) * limit
                difference = round(rounded - amount, 2)

                result.append(difference)
    investment_log.info("Суммирование")
    return f"{sum(result)} руб."


# if __name__ == "__main__":
#     data_func = date_analiz(input("В формате YYYY-MM -> "))
#     file_func = reading_excel_file(file)
#     limits = int(input("Введите лимит округления -> "))
#     print(investment_bank(data_func, file_func, limits))


def simple_search(data: list, search: str) -> str:
    """Выполняет простой поиск по категориям или описанию"""

    result = []
    simple_search_1_log.info("Запуск функции простого поиска")
    for operation in data:

        category = str(operation["Категория"]).lower()
        description = str(operation["Описание"]).lower()

        if category == search or description == search:
            result.append(operation)
    simple_search_1_log.info("Фильтрация операций")
    return json.dumps(result, ensure_ascii=False, indent=4)


# if __name__ == '__main__':
#     func_data = reading_excel_file(file)
#     str_search = input('Введите слово для поиска -> ').lower()
#     print(simple_search(func_data, str_search))


def phone_number_search(data: list) -> str:
    """Выводит все Транзакции, где телефон указан в описании"""

    phone_number_log.info("Запуск функции по поиску транзакций на номер телефона")
    pattern = r"\+7\s\d{3}\s\d{3}-\d{2}-\d{2}"
    result = []
    phone_number_log.info("Фильтрация операций")
    for operation in data:
        if re.search(pattern, operation["Описание"]):
            result.append(operation)

    return json.dumps(result, ensure_ascii=False, indent=4)


# if __name__ == '__main__':
#     func_data = reading_excel_file(file)
#     print(phone_number_search(func_data))


def search_for_individuals(data: List[Dict[str, Any]]) -> str:
    """Поиск переводов физическим лицам"""
    search_individuals_log.info("Запуск функции по переводам физ. лицам")
    pattern = r"\w{4,11}\s\w\.$"
    result = []
    search_individuals_log.info("Фильтрация операций")
    for operation in data:
        if re.search(pattern, operation["Описание"]):
            result.append(operation)

    return json.dumps(result, ensure_ascii=False, indent=4)


# if __name__ == '__main__':
#     func_data = reading_excel_file(file)
#     print(search_for_individuals(func_data))
