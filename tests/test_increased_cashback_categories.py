import pytest
import json
from datetime import datetime
from unittest.mock import patch
from src.services import increased_cashback_categories, cashback_log


class TestIncreasedCashbackCategories:
    """Тесты для функции анализа кэшбэка"""

    @pytest.fixture
    def sample_data(self):
        """Фикстура с тестовыми данными"""
        return [
            {
                "Дата операции": "01.01.2024 12:00:00",
                "Категория": "Еда",
                "Кэшбэк": 5.0,
                "Бонусы (включая кэшбэк)": 10.0
            },
            {
                "Дата операции": "05.01.2024 15:00:00",
                "Категория": "Транспорт",
                "Кэшбэк": 3.0,
                "Бонусы (включая кэшбэк)": 8.0
            },
            {
                "Дата операции": "10.01.2024 18:00:00",
                "Категория": "Развлечения",
                "Кэшбэк": None,
                "Бонусы (включая кэшбэк)": 15.0
            }
        ]

    def test_increased_cashback_categories_success(self, sample_data):
        """Тестирование успешного анализа кэшбэка"""
        result = increased_cashback_categories(sample_data, "01.2024")
        result_data = json.loads(result)

        assert "Еда" in result_data
        assert "Транспорт" in result_data
        assert "Развлечения" in result_data
        assert result_data["Еда"] == 15.0  # 5.0 + 10.0
        assert result_data["Транспорт"] == 11.0  # 3.0 + 8.0
        assert result_data["Развлечения"] == 15.0

    def test_increased_cashback_categories_wrong_date(self, sample_data):
        """Тестирование с неправильной датой"""
        result = increased_cashback_categories(sample_data, "02.2024")
        result_data = json.loads(result)

        assert result_data == {}  # Пустой словарь если нет данных за период

    def test_increased_cashback_categories_empty_data(self):
        """Тестирование с пустыми данными"""
        result = increased_cashback_categories([], "01.2024")
        result_data = json.loads(result)

        assert result_data == {}

    def test_increased_cashback_categories_no_cashback(self):
        """Тестирование когда нет кэшбэка"""
        data_no_cashback = [
            {
                "Дата операции": "01.01.2024 12:00:00",
                "Категория": "Еда",
                "Кэшбэк": None,
                "Бонусы (включая кэшбэк)": 0.0
            }
        ]

        result = increased_cashback_categories(data_no_cashback, "01.2024")
        result_data = json.loads(result)

        assert result_data == {}  # Пустой словарь если нет кэшбэка и бонусов

    @patch.object(cashback_log, 'info')
    def test_increased_cashback_categories_logging(self, mock_info, sample_data):
        """Тестирование логирования"""
        increased_cashback_categories(sample_data, "01.2024")

        assert mock_info.call_count >= 3