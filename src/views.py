import json
from datetime import datetime, time

from src.utils import apilayer_current, home_page_log, stock_prices, times_of_day_log, top_trans_log
from utils import date_analiz, reading_excel_file

file = r"C:\PythonProgramm\PROJECT\CourseWork\date\operations.xlsx"
#

def times_of_day(date_user: datetime) -> str:
    """Определения время суток"""
    times_of_day_log.info("Запуск функции определения времени суток")
    if date_user == "Неверный формат даты":
        times_of_day_log.error("Не верный формат даты")
        return date_user

    current_hour = date_user.hour
    times_of_day_log.info("Определение времени")

    if 5 <= current_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_hour < 17:
        greeting = "Добрый день"
    elif 17 <= current_hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    return greeting


def top_trans(date_user: datetime, data: list) -> list | str:
    """Топ-5 транзакций по сумме платежа"""
    top_trans_log.info("Запуск функции фильтрации и сортировки транзакций")
    all_transaction = []
    result = []
    start_time = datetime(date_user.year, date_user.month, 1)
    top_trans_log.info("Определение начало отсчета даты")
    end_data = date_user

    for operation in data:
        if operation["Номер карты"] is not None:

            date_file = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if start_time <= date_file <= end_data:
                top_trans_log.info("Сортировка по периоду")
                all_transaction.append(operation)

            if not all_transaction:
                top_trans_log.error("За выбранный период нет трат")
                return "За выбранный период нет трат"
    top_trans_log.info("Сортировка по тратам")
    top_5 = sorted(all_transaction, key=lambda x: x["Сумма операции с округлением"], reverse=True)[:5]

    top_trans_log.info("Преобразование в словарь")
    for top in top_5:

        formatted_results = {
            "date": top["Дата платежа"],
            "amount": top["Сумма операции с округлением"],
            "category": top["Категория"],
            "description": top["Описание"],
        }
        result.append(formatted_results)

    return result


def home_page(date_user: datetime, data: list) -> str | list:
    result = {"greeting": times_of_day(date_user)}
    home_page_log.info("Добавление времени суток")

    start_time = datetime.combine(date_user.date(), time(0, 0, 0))
    end_data = date_user
    home_page_log.info("Определение периода")
    cards_dict = {}

    home_page_log.info("Фильтрация")
    for operation in data:

        if operation["Номер карты"]:
            try:
                date_file = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")

                if start_time <= date_file <= end_data:

                    if float(operation["Сумма операции"]) < 0:
                        amount = abs(float(operation["Сумма операции"]))
                        last_digits = (operation["Номер карты"]).replace("*", "")

                        if last_digits not in cards_dict:
                            cards_dict[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}

                        cards_dict[last_digits]["total_spent"] += amount
                        cards_dict[last_digits]["cashback"] = round(cards_dict[last_digits]["total_spent"] / 100, 2)

            except (ValueError, TypeError, KeyError):
                home_page_log.error("Ошибка данных, пропуск значения")
                continue

    if not cards_dict:
        result["cards"] = "За выбранный период нет трат"
    else:
        result["cards"] = list(cards_dict.values())

    home_page_log.info("Добавление данных")
    result["top_transactions"] = top_trans(date_user, data)
    result["currency_rates"] = apilayer_current()
    result["stock_prices"] = stock_prices()

    return json.dumps(result, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
#
#     func_date = date_analiz("31.12.2021 23:44:00")
#     func_file = reading_excel_file(file)
#     print(home_page(func_date, func_file))
