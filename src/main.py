import pandas as pd

from services import (increased_cashback_categories, investment_bank, phone_number_search, search_for_individuals,
                      simple_search)
from src.reports import spending_by_category
from src.utils import date_analiz, reading_excel_file
from src.views import home_page

file = r"C:\PythonProgramm\PROJECT\CourseWork\date\operations.xlsx"

if __name__ == "__main__":
    """Запуск всех функций уже с выбранными параметрами для некоторых функций"""

    func_file = reading_excel_file(file)
    func_date = date_analiz("2020-1")
    func_date1 = date_analiz("31.12.2021 23:44:00")
    word = "ТаксовичкоФ".lower()

    print("-" * 100)
    print("Функция считает выгоду кэшбэка за месяц:")
    print(increased_cashback_categories(func_file, func_date))

    print("-" * 100)
    print("Инвесткопилка с лимитом округления 50:\n")
    print(investment_bank(func_date, func_file, limit=50), "за 07.2020 можно было бы накопить")

    print("-" * 100)
    print("Функция простого поиска уже с заданным словом:")
    print(simple_search(func_file, word))

    print("-" * 100)
    print("Функция выводит все операции с номерами телефонов в описании:")
    print(phone_number_search(func_file))

    print("-" * 100)
    print("Функция выводит все операции физ. лицам:")
    print(search_for_individuals(func_file))
    print("-" * 100)

    print("Страница Главная")
    print(home_page(func_date1, func_file))
    print("-" * 100)

    print("Страница Отчеты")
    # Загружаем данные из Excel
    df = pd.read_excel(r"C:\PythonProgramm\PROJECT\CourseWork\date\operations.xlsx", sheet_name="Отчет по операциям")

    # С автоматическим именем файла
    result_df = spending_by_category(df, "Супермаркеты", "31.12.2021")

    # Можно сначала посмотреть результат в переменной
    print(result_df[["Дата операции", "Сумма операции", "Описание"]].head())
    print("-" * 100)
