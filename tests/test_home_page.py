import pytest
import json
from datetime import datetime, time
from unittest.mock import patch, MagicMock
from src.views import home_page, home_page_log, times_of_day, top_trans, apilayer_current, stock_prices


class TestHomePage:
    """Тесты для функции домашней страницы"""

    @pytest.fixture
    def sample_data(self):
        """Фикстура с тестовыми данными"""
        return [
            {
                "Номер карты": "1234****5678",
                "Дата операции": "01.01.2024 12:00:00",
                "Сумма операции": "-1000.50",
                "Категория": "Еда"
            },
            {
                "Номер карты": "9876****5432",
                "Дата операции": "01.01.2024 14:00:00",
                "Сумма операции": "-2000.75",
                "Категория": "Транспорт"
            },
            {
                "Номер карты": None,
                "Дата операции": "01.01.2024 16:00:00",
                "Сумма операции": "-500.25",
                "Категория": "Развлечения"
            }
        ]

    @patch('src.views.times_of_day')
    @patch('src.views.top_trans')
    @patch('src.views.apilayer_current')
    @patch('src.views.stock_prices')
    def test_home_page_with_valid_data(self, mock_stock, mock_currency, mock_top_trans, mock_times_of_day, sample_data):
        """Тестирование с валидными данными"""
        mock_times_of_day.return_value = "Добрый день"
        mock_top_trans.return_value = [{"amount": 1000}]
        mock_currency.return_value = {"USD": 75.0}
        mock_stock.return_value = {"AAPL": 150.0}

        test_date = datetime(2024, 1, 1, 15, 0, 0)
        result = home_page(test_date, sample_data)
        result_data = json.loads(result)

        assert result_data["greeting"] == "Добрый день"
        assert len(result_data["cards"]) == 2
        assert result_data["top_transactions"] == [{"amount": 1000}]
        assert result_data["currency_rates"] == {"USD": 75.0}
        assert result_data["stock_prices"] == {"AAPL": 150.0}

    @patch('src.views.times_of_day')
    @patch('src.views.top_trans')
    @patch('src.views.apilayer_current')
    @patch('src.views.stock_prices')
    def test_home_page_no_transactions(self, mock_stock, mock_currency, mock_top_trans, mock_times_of_day):
        """Тестирование когда нет транзакций"""
        mock_times_of_day.return_value = "Добрый день"
        mock_top_trans.return_value = []
        mock_currency.return_value = {}
        mock_stock.return_value = {}

        test_date = datetime(2024, 1, 1, 15, 0, 0)
        result = home_page(test_date, [])
        result_data = json.loads(result)

        assert result_data["cards"] == "За выбранный период нет трат"
        assert result_data["top_transactions"] == []

    @patch('src.views.times_of_day')
    @patch('src.views.top_trans')
    @patch('src.views.apilayer_current')
    @patch('src.views.stock_prices')
    def test_home_page_only_positive_transactions(self, mock_stock, mock_currency, mock_top_trans, mock_times_of_day):
        """Тестирование когда только положительные транзакции"""
        mock_times_of_day.return_value = "Добрый день"
        mock_top_trans.return_value = []
        mock_currency.return_value = {}
        mock_stock.return_value = {}

        data_positive = [{
            "Номер карты": "1234****5678",
            "Дата операции": "01.01.2024 12:00:00",
            "Сумма операции": "1000.50",
            "Категория": "Еда"
        }]

        test_date = datetime(2024, 1, 1, 15, 0, 0)
        result = home_page(test_date, data_positive)
        result_data = json.loads(result)

        assert result_data["cards"] == "За выбранный период нет трат"

    @patch('src.views.times_of_day')
    @patch('src.views.top_trans')
    @patch('src.views.apilayer_current')
    @patch('src.views.stock_prices')
    def test_home_page_only_none_card_numbers(self, mock_stock, mock_currency, mock_top_trans, mock_times_of_day):
        """Тестирование когда у всех операций нет номера карты"""
        mock_times_of_day.return_value = "Добрый день"
        mock_top_trans.return_value = []
        mock_currency.return_value = {}
        mock_stock.return_value = {}

        data_none_cards = [{
            "Номер карты": None,
            "Дата операции": "01.01.2024 12:00:00",
            "Сумма операции": "-1000.50",
            "Категория": "Еда"
        }]

        test_date = datetime(2024, 1, 1, 15, 0, 0)
        result = home_page(test_date, data_none_cards)
        result_data = json.loads(result)

        assert result_data["cards"] == "За выбранный период нет трат"

    @patch.object(home_page_log, 'info')
    @patch.object(home_page_log, 'error')
    @patch('src.views.times_of_day')
    @patch('src.views.top_trans')
    @patch('src.views.apilayer_current')
    @patch('src.views.stock_prices')
    def test_home_page_logging(self, mock_stock, mock_currency, mock_top_trans, mock_times_of_day, mock_error, mock_info):
        """Тестирование логирования"""
        mock_times_of_day.return_value = "Добрый день"
        mock_top_trans.return_value = []
        mock_currency.return_value = {}
        mock_stock.return_value = {}

        test_date = datetime(2024, 1, 1, 15, 0, 0)
        home_page(test_date, [])

        assert mock_info.call_count >= 3