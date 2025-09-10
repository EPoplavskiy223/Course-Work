import json
import logging
import os
from datetime import datetime
from typing import Any, List, Union

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

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
date_analiz_log = logging.getLogger("name.date_analiz_log")
convector_json_log = logging.getLogger("name.convector_json_log")
apilayer_current_log = logging.getLogger("name.apilayer_current_log")
stock_prices_log = logging.getLogger("name.stock_prices_log")
times_of_day_log = logging.getLogger("name.times_of_day_log")
top_trans_log = logging.getLogger("name.top_trans_log")
home_page_log = logging.getLogger("name.home_page_log")

file = r"C:\PythonProgramm\PROJECT\CourseWork\date\operations.xlsx"


def date_analiz(full_date: str) -> datetime | str:
    """Анализирует вводимую дату и время"""
    date_analiz_log.info("Запуск функции анализа данных")
    base = {
        "analiz": [
            "%Y-%m-%d %H:%M:%S",  # 2024-01-15 14:30:00
            "%Y-%m-%d %H:%M",  # 2024-01-15 14:30
            "%Y-%m-%d",  # 2024-01-15
            "%d.%m.%Y %H:%M:%S",  # 15.01.2024 14:30:00
            "%d.%m.%Y %H:%M",  # 15.01.2024 14:30
            "%d.%m.%Y",  # 15.01.2024
            "%m.%Y %H:%M:%S",  # 01.2024 14:30:00
            "%m.%Y %H:%M",  # 01.2024 14:30
            "%m.%Y",  # 01.2024
            "%Y-%m",  # 2024-01
            "%m.%Y",  # 01.2024
        ]
    }

    for fmt in base["analiz"]:
        try:
            dt = datetime.strptime(full_date, fmt)
            date_analiz_log.info("Преобразование формата даты")
            if ":" in fmt:
                if "%d" in fmt:
                    date_analiz_log.info("Успешное сравнение с базой дат")
                    return dt
                else:
                    date_analiz_log.info("Успешное сравнение с базой дат")
                    return dt
            elif "%d" in fmt:
                date_analiz_log.info("Успешное сравнение с базой дат")
                return dt.strftime("%d.%m.%Y")
            else:
                date_analiz_log.info("Успешное сравнение с базой дат")
                return dt.strftime("%m.%Y")

        except ValueError:
            date_analiz_log.info("Ошибка. Не удалось преобразовать")
            continue

    return "Неверный формат даты"


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


def convector_json(file_path: str) -> list | dict | str:
    """Конвертирует json файл"""
    try:
        convector_json_log.info("Запуск функции чтения JSON формата")
        with open(file_path, "r", encoding="utf-8") as json_file:
            convector_json_log.info("Успешное прочтение")
            data = json.load(json_file)
            convector_json_log.info("Успешно преобразован")
            return data  # type: ignore[no-any-return]

    except json.JSONDecodeError:
        convector_json_log.error("Файл пустой! Или не содержит .json")
        return ["Файл пустой! Или не содержит .json"]

    except FileNotFoundError:
        convector_json_log.error("Файл не найден")
        return ["Файл не найден"]

    except UnicodeDecodeError:
        convector_json_log.error("Не правильный формат файла")
        return ["Не правильный формат файла"]


def apilayer_current() -> dict | list:
    """Конвертирование валют в рубли"""
    apilayer_current_log.info("Запуск функции конвертации валют")
    load_dotenv()
    api_key = os.getenv("APILayer_key")
    apilayer_current_log.info("Получение ключа API")
    headers = {"apikey": api_key}

    result = []

    user_settings = convector_json(r"C:\PythonProgramm\PROJECT\CourseWork\user_settings.json")

    for param in user_settings["user_currencies"]:
        apilayer_current_log.info("Запрос на выбранную валюту")

        url = f"https://api.apilayer.com/exchangerates_data/latest?base={param}"

        response = requests.get(url, headers=headers)
        apilayer_current_log.info("Форматирование ответа")
        data = response.json()

        result.append({"currency": param, "rate": data["rates"]["RUB"]})
        apilayer_current_log.info("Добавление в словарь")

    return result


def stock_prices() -> dict | list:
    """Стоимость акций из S&P500"""

    data = convector_json(r"C:\PythonProgramm\PROJECT\CourseWork\user_settings.json")
    stock_prices_log.info("Запуск функции цен акций")
    user_stocks = data["user_stocks"]

    result = []
    for ticker in user_stocks:
        stock = yf.Ticker(ticker)
        info = stock.info
        stock_prices_log.info("Получение название акции")

        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")

        if current_price is not None:
            result.append({"stock": ticker, "price": round(current_price, 2)})

    return result
