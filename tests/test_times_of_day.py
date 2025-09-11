import pytest
import sys
import os
from datetime import datetime
from unittest.mock import patch

from src.utils import times_of_day_log
from src.views import times_of_day


class TestTimesOfDay:
    """Тесты для функции определения времени суток"""

    @pytest.mark.parametrize("hour,expected_greeting", [
        (5, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (16, "Добрый день"),
        (17, "Добрый вечер"),
        (21, "Добрый вечер"),
        (22, "Доброй ночи"),
        (4, "Доброй ночи"),
        (0, "Доброй ночи")
    ])
    def test_times_of_day_with_different_hours(self, hour, expected_greeting):
        """Тестирование разных часов времени суток"""
        test_date = datetime(2024, 1, 1, hour)
        result = times_of_day(test_date)
        assert result == expected_greeting

    def test_times_of_day_with_invalid_format(self):
        """Тестирование с неверным форматом даты"""
        result = times_of_day("Неверный формат даты")
        assert result == "Неверный формат даты"

    @patch.object(times_of_day_log, 'info')
    @patch.object(times_of_day_log, 'error')
    def test_logging_with_invalid_format(self, mock_error, mock_info):
        """Тестирование логирования при неверном формате"""
        times_of_day("Неверный формат даты")
        mock_error.assert_called_once_with("Не верный формат даты")

    @patch.object(times_of_day_log, 'info')
    def test_logging_with_valid_date(self, mock_info):
        """Тестирование логирования при валидной дате"""
        test_date = datetime(2024, 1, 1, 10)
        times_of_day(test_date)
        assert mock_info.call_count == 2