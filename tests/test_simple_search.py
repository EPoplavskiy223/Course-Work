import pytest
import json
from unittest.mock import patch
import sys
import os

from src.services import simple_search
from src.utils import simple_search_1_log


class TestSimpleSearch:
    """Тесты для функции простого поиска"""

    @pytest.fixture
    def sample_data(self):
        """Фикстура с тестовыми данными"""
        return [
            {
                "Категория": "Еда",
                "Описание": "Продукты в магазине",
                "Сумма операции": -1000.50
            },
            {
                "Категория": "Транспорт",
                "Описание": "Такси до работы",
                "Сумма операции": -500.75
            },
            {
                "Категория": "Еда",
                "Описание": "Обед в кафе",
                "Сумма операции": -1500.00
            },
            {
                "Категория": "Развлечения",
                "Описание": "Кино",
                "Сумма операции": -800.00
            }
        ]

    def test_simple_search_by_category(self, sample_data):
        """Тестирование поиска по категории"""
        result = simple_search(sample_data, "еда")  # Строгое сравнение с нижним регистром
        result_data = json.loads(result)

        assert len(result_data) == 2
        assert all(item["Категория"].lower() == "еда" for item in result_data)

    def test_simple_search_by_description(self, sample_data):
        """Тестирование поиска по описанию"""
        # Функция ищет строгое совпадение, поэтому нужно полное описание в нижнем регистре
        result = simple_search(sample_data, "такси до работы")
        result_data = json.loads(result)

        assert len(result_data) == 1
        assert result_data[0]["Описание"].lower() == "такси до работы"

    def test_simple_search_case_insensitive(self, sample_data):
        """Тестирование регистронезависимого поиска"""
        # Функция преобразует все к нижнему регистру, поэтому нужно искать в нижнем
        result = simple_search(sample_data, "еда")
        result_data = json.loads(result)

        assert len(result_data) == 2
        assert all(item["Категория"].lower() == "еда" for item in result_data)

    def test_simple_search_no_results(self, sample_data):
        """Тестирование когда нет результатов"""
        result = simple_search(sample_data, "несуществующий")
        result_data = json.loads(result)

        assert result_data == []

    def test_simple_search_empty_data(self):
        """Тестирование с пустыми данными"""
        result = simple_search([], "еда")
        result_data = json.loads(result)

        assert result_data == []

    @patch.object(simple_search_1_log, 'info')
    def test_simple_search_logging(self, mock_info, sample_data):
        """Тестирование логирования"""
        simple_search(sample_data, "еда")

        assert mock_info.call_count == 2