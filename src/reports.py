from datetime import datetime, timedelta

import pandas as pd


def save_report(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if filename is None:
                from datetime import datetime

                report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            else:
                report_name = filename

            with open(report_name, "w", encoding="utf-8") as f:
                if hasattr(result, "to_string"):
                    f.write(result.to_string())
                else:
                    f.write(str(result))

            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:

    if date is None:
        date = datetime.now().strftime("%d.%m.%Y")

    end_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = end_date - timedelta(days=90)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    filtered_data = transactions[
        (transactions["Категория"] == category)
        & (transactions["Сумма операции"] < 0)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]

    return filtered_data
