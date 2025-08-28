import json
import logging
import math
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pandas as pd

file = r"C:\PythonProgramm\PROJECT\CourseWork\date\operations.xlsx"

# Настройка логгера
logger = logging.getLogger("name")

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    r"C:\PythonProgramm\PROJECT\CourseWork\logs\service.log", mode="w", encoding="utf-8"
)

file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

excel_log = logging.getLogger("name.reading_excel_file")
cashback_log = logging.getLogger("name.increased_cashback_categories")
date_log = logging.getLogger("name.user_data")
investment_log = logging.getLogger("name.investment_bank")
simple_search_1_log = logging.getLogger("name.simple_search")
phone_number_log = logging.getLogger("name.phone_number_search")
search_individuals_log = logging.getLogger("name.search_for_individuals")


def reading_excel_file(data: str) -> Union[List[Any], str]:
    """Чтение excel файла"""
    excel_log.info("Запуск функции чтения файлов")

    try:
        df_excel = pd.read_excel(data)
        list_excel = df_excel.to_dict("records")
        for record in list_excel:
            for key in record:
                if pd.isna(record[key]):
                    record[key] = None
        excel_log.info("Файл успешно прочитан и конвертирован")
        return list_excel

    except UnicodeDecodeError:
        excel_log.error("ошибка в чтении файла")
        return "Ошибка! Файл не читается"


def check_date_user(date: str, year: Optional[str] = None) -> str:
    """Проверка выбранного периода пользователем"""
    if date and year:
        try:
            dt = datetime.strptime(f"01.{date}.{year}", "%d.%m.%Y")
            date_user = dt.strftime("%m.%Y")
            date_log.info("Успешное преобразование выбранного периода")
            return date_user
        except ValueError:
            date_log.error("Неверный формат даты")
            return "Ошибка: неверный формат месяца или года"
    else:
        try:
            dt = datetime.strptime(f"{date}-01", "%Y-%m-%d")
            date_user = dt.strftime("%m.%Y")
            date_log.info("Успешное преобразование выбранного периода")
            return date_user
        except ValueError:
            date_log.error("Неверный формат даты")
            return "Ошибка: неверный формат месяца или года"


def increased_cashback_categories(data: list[dict], date_user: str) -> str:
    """Анализ выгодных категорий повышенного кешбэка"""

    cashback_log.info("Запуск функции анализа кешбэка")

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
#     func_date = check_date_user(date=input('Введите месяц -> '), year=input('Введите год -> '))
#     func_data = reading_excel_file(file)
#     print(increased_cashback_categories(func_data, func_date))


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """Инвесткопилка"""

    investment_log.info("Запуск функции инвесткопилки")
    result = []
    investment_log.info("Фильтрация трат от пополнений")
    for transaction in transactions:
        if datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y") == month:
            if transaction["Сумма операции"] < 0:

                amount = transaction["Сумма операции"] * -1

                rounded = math.ceil(amount / limit) * limit
                difference = round(rounded - amount, 2)

                result.append(difference)
    investment_log.info("Суммирование")
    return f"{sum(result)} руб."


# if __name__ == "__main__":
#     data_func = check_date_user(input("В формате YYYY-MM -> "))
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
