import pytest
import os
from unittest.mock import patch, Mock
from src.utils import apilayer_current, apilayer_current_log


class TestApilayerCurrent:
    """Тесты для функции конвертации валют"""

    @patch('src.utils.convector_json')
    @patch('src.utils.requests.get')
    @patch.dict(os.environ, {'APILayer_key': 'test_api_key'})
    def test_apilayer_current_success(self, mock_get, mock_convector_json):
        """Тестирование успешного получения курсов валют"""
        # Мокируем настройки пользователя
        mock_convector_json.return_value = {
            "user_currencies": ["USD", "EUR"]
        }

        # Мокируем ответы API
        mock_response_usd = Mock()
        mock_response_usd.json.return_value = {"rates": {"RUB": 75.5}}
        mock_response_eur = Mock()
        mock_response_eur.json.return_value = {"rates": {"RUB": 85.3}}

        mock_get.side_effect = [mock_response_usd, mock_response_eur]

        result = apilayer_current()

        assert len(result) == 2
        assert result[0]["currency"] == "USD"
        assert result[0]["rate"] == 75.5
        assert result[1]["currency"] == "EUR"
        assert result[1]["rate"] == 85.3

    @patch('src.utils.convector_json')
    @patch.dict(os.environ, {'APILayer_key': 'test_api_key'})
    def test_apilayer_current_no_currencies(self, mock_convector_json):
        """Тестирование когда нет выбранных валют"""
        mock_convector_json.return_value = {
            "user_currencies": []
        }

        result = apilayer_current()

        assert result == []

    @patch('src.utils.convector_json')
    @patch('src.utils.requests.get')
    @patch.dict(os.environ, {'APILayer_key': 'test_api_key'})
    def test_apilayer_current_api_error(self, mock_get, mock_convector_json):
        """Тестирование ошибки API"""
        mock_convector_json.return_value = {
            "user_currencies": ["USD"]
        }

        mock_get.side_effect = Exception("API error")

        # Ожидаем, что функция выбросит исключение
        with pytest.raises(Exception, match="API error"):
            apilayer_current()

    @patch.object(apilayer_current_log, 'info')
    @patch('src.utils.convector_json')
    @patch('src.utils.requests.get')
    @patch.dict(os.environ, {'APILayer_key': 'test_api_key'})
    def test_apilayer_current_logging(self, mock_get, mock_convector_json, mock_info):
        """Тестирование логирования"""
        mock_convector_json.return_value = {
            "user_currencies": ["USD"]
        }

        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}
        mock_get.return_value = mock_response

        apilayer_current()

        assert mock_info.call_count >= 4