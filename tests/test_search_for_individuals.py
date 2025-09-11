import pytest
import json
import re
from unittest.mock import patch
from src.services import search_for_individuals
from src.utils import search_individuals_log


class TestSearchForIndividuals:

    @pytest.fixture
    def sample_data(self):
        return [
            {
                "Описание": "Иванов И.",
                "Сумма операции": -5000.00,
                "Категория": "Перевод"
            },
            {
                "Описание": "Петров П.",
                "Сумма операции": -3000.00,
                "Категория": "Перевод"
            },
            {
                "Описание": "Оплата услуг",
                "Сумма операции": -1000.50,
                "Категория": "Услуги"
            },
            {
                "Описание": "Сидоров А.",
                "Сумма операции": -2000.00,
                "Категория": "Перевод"
            }
        ]

    def test_search_for_individuals_found(self, sample_data):
        result = search_for_individuals(sample_data)
        result_data = json.loads(result)

        assert len(result_data) == 3
        for item in result_data:
            assert re.search(r"\w{4,11}\s\w\.$", item["Описание"])

    def test_search_for_individuals_not_found(self):
        data_without_individuals = [
            {
                "Описание": "Оплата услуг",
                "Сумма операции": -1000.50
            },
            {
                "Описание": "Пополнение счета",
                "Сумма операции": 5000.00
            }
        ]

        result = search_for_individuals(data_without_individuals)
        result_data = json.loads(result)

        assert result_data == []

    def test_search_for_individuals_empty_data(self):
        result = search_for_individuals([])
        result_data = json.loads(result)

        assert result_data == []

    def test_search_for_individuals_various_formats(self):
        various_formats_data = [
            {
                "Описание": "Иван И.",
                "Сумма операции": -1000.00,
                "Категория": "Перевод"
            },
            {
                "Описание": "Оченьдлн И.",
                "Сумма операции": -2000.00,
                "Категория": "Перевод"
            },
            {
                "Описание": "Петров П.С.",
                "Сумма операции": -3000.00,
                "Категория": "Перевод"
            },
            {
                "Описание": "Смирнов В.",
                "Сумма операции": -4000.00,
                "Категория": "Перевод"
            }
        ]

        result = search_for_individuals(various_formats_data)
        result_data = json.loads(result)

        assert len(result_data) == 3
        descriptions = [item["Описание"] for item in result_data]
        assert "Иван И." in descriptions
        assert "Оченьдлн И." in descriptions
        assert "Смирнов В." in descriptions
        assert "Петров П.С." not in descriptions

    @patch.object(search_individuals_log, 'info')
    def test_search_for_individuals_logging(self, mock_info, sample_data):
        search_for_individuals(sample_data)

        assert mock_info.call_count == 2