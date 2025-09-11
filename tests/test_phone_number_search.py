import pytest
import json
import re
from unittest.mock import patch
from src.services import phone_number_search
from src.utils import phone_number_log


class TestPhoneNumberSearch:
    """Тесты для функции поиска транзакций по номеру телефона"""

    @pytest.fixture
    def sample_data(self):
        """Фикстура с тестовыми данными"""
        return [
            {
                "Описание": "Оплата услуг +7 999 123-45-67",
                "Сумма операции": -1000.50,
                "Категория": "Связь"
            },
            {
                "Описание": "Перевод на карту",
                "Сумма операции": -5000.00,
                "Категория": "Перевод"
            },
            {
                "Описание": "Оплата мобильного +7 888 765-43-21",
                "Сумма операции": -500.00,
                "Категория": "Связь"
            },
            {
                "Описание": "Пополнение телефона +7 777 111-22-33",
                "Сумма операции": -300.00,
                "Категория": "Связь"
            }
        ]

    def test_phone_number_search_found(self, sample_data):
        """Тестирование когда найдены транзакции с номерами"""
        result = phone_number_search(sample_data)
        result_data = json.loads(result)

        assert len(result_data) == 3

        for item in result_data:
            assert re.search(r"\+7\s\d{3}\s\d{3}-\d{2}-\d{2}", item["Описание"])

    def test_phone_number_search_not_found(self):
        """Тестирование когда нет транзакций с номерами"""
        data_without_phones = [
            {
                "Описание": "Оплата услуг",
                "Сумма операции": -1000.50
            },
            {
                "Описание": "Перевод на карту",
                "Сумма операции": -5000.00
            }
        ]

        result = phone_number_search(data_without_phones)
        result_data = json.loads(result)

        assert result_data == []

    def test_phone_number_search_empty_data(self):
        """Тестирование с пустыми данными"""
        result = phone_number_search([])
        result_data = json.loads(result)

        assert result_data == []

    def test_phone_number_search_different_formats(self):
        """Тестирование с разными форматами номеров"""
        data_with_different_formats = [
            {
                "Описание": "Неправильный формат +79991234567",
                "Сумма операции": -1000.50
            },
            {
                "Описание": "Правильный формат +7 999 123-45-67",
                "Сумма операции": -500.00
            }
        ]

        result = phone_number_search(data_with_different_formats)
        result_data = json.loads(result)

        assert len(result_data) == 1
        assert result_data[0]["Описание"] == "Правильный формат +7 999 123-45-67"

    @patch.object(phone_number_log, 'info')
    def test_phone_number_search_logging(self, mock_info, sample_data):
        """Тестирование логирования"""
        phone_number_search(sample_data)

        assert mock_info.call_count == 2