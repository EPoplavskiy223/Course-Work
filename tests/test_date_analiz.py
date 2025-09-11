import pytest
from datetime import datetime
from unittest.mock import patch
from src.utils import date_analiz, date_analiz_log


class TestDateAnaliz:
    """Тесты для функции анализа даты"""

    @pytest.mark.parametrize("input_date,expected", [
        ("2024-01-15 14:30:00", datetime(2024, 1, 15, 14, 30, 0)),
        ("2024-01-15 14:30", datetime(2024, 1, 15, 14, 30, 0)),
        ("15.01.2024 14:30:00", datetime(2024, 1, 15, 14, 30, 0)),
        ("15.01.2024 14:30", datetime(2024, 1, 15, 14, 30, 0)),
        ("2024-01-15", "15.01.2024"),
        ("15.01.2024", "15.01.2024"),
        ("01.2024 14:30:00", datetime(2024, 1, 1, 14, 30, 0)),
        ("01.2024 14:30", datetime(2024, 1, 1, 14, 30, 0)),
        ("01.2024", "01.2024"),
        ("2024-01", "01.2024")
    ])
    def test_date_analiz_valid_formats(self, input_date, expected):
        """Тестирование валидных форматов даты"""
        result = date_analiz(input_date)
        assert result == expected

    def test_date_analiz_invalid_format(self):
        """Тестирование неверного формата даты"""
        result = date_analiz("invalid-date")
        assert result == "Неверный формат даты"

    @patch.object(date_analiz_log, 'info')
    def test_date_analiz_logging_valid(self, mock_info):
        """Тестирование логирования при валидной дате"""
        date_analiz("2024-01-15 14:30:00")
        assert mock_info.call_count >= 3

    @patch.object(date_analiz_log, 'info')
    def test_date_analiz_logging_invalid(self, mock_info):
        """Тестирование логирования при невалидной дате"""
        date_analiz("invalid-date")
        assert mock_info.call_count >= 2