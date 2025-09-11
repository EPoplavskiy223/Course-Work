import pytest
import math
from datetime import datetime
from unittest.mock import patch
import sys
import os

from src.services import investment_bank
from src.utils import investment_log


class TestInvestmentBank:
    """Тесты для функции инвесткопилки"""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями"""
        return [
            {
                "Дата операции": "01.01.2024 12:00:00",
                "Сумма операции": -1500.50,
                "Категория": "Еда"
            },
            {
                "Дата операции": "05.01.2024 15:00:00",
                "Сумма операции": -2750.30,
                "Категория": "Транспорт"
            },
            {
                "Дата операции": "10.01.2024 18:00:00",
                "Сумма операции": 5000.00,
                "Категория": "Пополнение"
            },
            {
                "Дата операции": "15.01.2024 09:00:00",
                "Сумма операции": -999.99,
                "Категория": "Развлечения"
            }
        ]

    def test_investment_bank_success(self, sample_transactions):
        """Тестирование успешного расчета инвесткопилки"""
        result = investment_bank("01.2024", sample_transactions, 100)

        assert result == "149.21 руб."

    def test_investment_bank_different_limit(self, sample_transactions):
        """Тестирование с разным лимитом округления"""
        result = investment_bank("01.2024", sample_transactions, 50)

        result_value = float(result.split()[0])
        assert round(result_value, 2) == 99.21
        assert result.endswith("руб.")

    def test_investment_bank_wrong_date(self, sample_transactions):
        """Тестирование с неправильной датой"""
        result = investment_bank("02.2024", sample_transactions, 100)

        assert result == "0 руб."

    def test_investment_bank_only_positive_transactions(self):
        """Тестирование когда только положительные транзакции"""
        positive_transactions = [
            {
                "Дата операции": "01.01.2024 12:00:00",
                "Сумма операции": 1000.00,
                "Категория": "Пополнение"
            }
        ]

        result = investment_bank("01.2024", positive_transactions, 100)

        assert result == "0 руб."

    def test_investment_bank_empty_data(self):
        """Тестирование с пустыми данными"""
        result = investment_bank("01.2024", [], 100)

        assert result == "0 руб."

    @patch.object(investment_log, 'info')
    def test_investment_bank_logging(self, mock_info, sample_transactions):
        """Тестирование логирования"""
        investment_bank("01.2024", sample_transactions, 100)

        assert mock_info.call_count >= 3