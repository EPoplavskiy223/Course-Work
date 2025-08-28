from src.services import (check_date_user, increased_cashback_categories, investment_bank, phone_number_search,
                          reading_excel_file, search_for_individuals, simple_search)

file = r"C:\PythonProgramm\PROJECT\CourseWork\date\operations.xlsx"

if __name__ == "__main__":
    """Запуск всех функций уже с выбранными параметрами для некоторых функций"""

    func_file = reading_excel_file(file)
    func_date_1 = check_date_user(date="3", year="2020")
    func_date_2 = check_date_user("2020-7")
    word = "ТаксовичкоФ".lower()

    print("-" * 100)
    print("Функция считает выгоду кэшбэка за месяц:")
    print(increased_cashback_categories(func_file, func_date_1))

    print("-" * 100)
    print("Инвесткопилка с лимитом округления 50:\n")
    print(investment_bank(func_date_2, func_file, limit=50), "за 07.2020 можно было бы накопить")

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
