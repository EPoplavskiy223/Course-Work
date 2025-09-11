import pytest
from unittest.mock import patch, Mock
from src.utils import stock_prices, stock_prices_log


class TestStockPrices:
    """Тесты для функции получения цен акций"""

    @patch('src.utils.convector_json')
    @patch('src.utils.yf.Ticker')
    def test_stock_prices_success(self, mock_ticker, mock_convector_json):
        """Тестирование успешного получения цен акций"""
        # Мокируем настройки пользователя
        mock_convector_json.return_value = {
            "user_stocks": ["AAPL", "GOOGL"]
        }

        # Мокируем данные акций
        mock_aapl = Mock()
        mock_aapl.info = {"currentPrice": 150.50}
        mock_googl = Mock()
        mock_googl.info = {"regularMarketPrice": 2800.75}

        mock_ticker.side_effect = [mock_aapl, mock_googl]

        result = stock_prices()

        assert len(result) == 2
        assert result[0]["stock"] == "AAPL"
        assert result[0]["price"] == 150.50
        assert result[1]["stock"] == "GOOGL"
        assert result[1]["price"] == 2800.75

    @patch('src.utils.convector_json')
    @patch('src.utils.yf.Ticker')
    def test_stock_prices_different_price_fields(self, mock_ticker, mock_convector_json):
        """Тестирование с разными полями цен"""
        mock_convector_json.return_value = {
            "user_stocks": ["TSLA"]
        }

        mock_tesla = Mock()
        mock_tesla.info = {"previousClose": 250.30}  # Используем previousClose
        mock_ticker.return_value = mock_tesla

        result = stock_prices()

        assert result[0]["stock"] == "TSLA"
        assert result[0]["price"] == 250.30

    @patch('src.utils.convector_json')
    @patch('src.utils.yf.Ticker')
    def test_stock_prices_no_price_available(self, mock_ticker, mock_convector_json):
        """Тестирование когда цена недоступна"""
        mock_convector_json.return_value = {
            "user_stocks": ["NONE"]
        }

        mock_none = Mock()
        mock_none.info = {}  # Нет данных о цене
        mock_ticker.return_value = mock_none

        result = stock_prices()

        assert result == []  # Пустой список если цена None

    @patch('src.utils.convector_json')
    def test_stock_prices_no_stocks(self, mock_convector_json):
        """Тестирование когда нет выбранных акций"""
        mock_convector_json.return_value = {
            "user_stocks": []
        }

        result = stock_prices()

        assert result == []

    @patch.object(stock_prices_log, 'info')
    @patch('src.utils.convector_json')
    @patch('src.utils.yf.Ticker')
    def test_stock_prices_logging(self, mock_ticker, mock_convector_json, mock_info):
        """Тестирование логирования"""
        mock_convector_json.return_value = {
            "user_stocks": ["AAPL"]
        }

        mock_aapl = Mock()
        mock_aapl.info = {"currentPrice": 150.50}
        mock_ticker.return_value = mock_aapl

        stock_prices()

        assert mock_info.call_count >= 2