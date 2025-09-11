import pytest
from datetime import datetime
from unittest.mock import patch
from src.views import top_trans, top_trans_log


class TestTopTrans:
    """Тесты для функции топ-5 транзакций"""

    @pytest.fixture
    def sample_data(self):
        """Фикстура с тестовыми данными"""
        return [
            {
                "Номер карты": "1234",
                "Дата операции": "01.01.2024 12:00:00",
                "Дата платежа": "01.01.2024",
                "Сумма операции с округлением": 1000,
                "Категория": "Еда",
                "Описание": "Продукты"
            },
            {
                "Номер карты": "5678",
                "Дата операции": "05.01.2024 15:00:00",
                "Дата платежа": "05.01.2024",
                "Сумма операции с округлением": 5000,
                "Категория": "Транспорт",
                "Описание": "Такси"
            },
            {
                "Номер карты": None,
                "Дата операции": "10.01.2024 18:00:00",
                "Дата платежа": "10.01.2024",
                "Сумма операции с округлением": 3000,
                "Категория": "Развлечения",
                "Описание": "Кино"
            }
        ]

    def test_top_trans_with_valid_data(self, sample_data):
        """Тестирование с валидными данными"""
        test_date = datetime(2024, 1, 15)
        result = top_trans(test_date, sample_data)

        assert len(result) == 2
        assert result[0]["amount"] == 5000
        assert result[1]["amount"] == 1000

    def test_top_trans_no_transactions_in_period(self, sample_data):
        """Тестирование когда нет транзакций за период"""
        test_date = datetime(2023, 12, 1)
        result = top_trans(test_date, sample_data)

        assert result == "За выбранный период нет трат"

    def test_top_trans_empty_data(self):
        """Тестирование с пустым списком данных"""
        test_date = datetime(2024, 1, 15)
        result = top_trans(test_date, [])

        assert result == []  # Функция возвращает пустой список

    def test_top_trans_only_none_card_numbers(self):
        """Тестирование когда у всех операций нет номера карты"""
        data_with_none_cards = [
            {
                "Номер карты": None,
                "Дата операции": "01.01.2024 12:00:00",
                "Дата платежа": "01.01.2024",
                "Сумма операции с округлением": 1000,
                "Категория": "Еда",
                "Описание": "Продукты"
            }
        ]
        test_date = datetime(2024, 1, 15)
        result = top_trans(test_date, data_with_none_cards)

        assert result == []  # Функция возвращает пустой список

    @patch.object(top_trans_log, 'info')
    @patch.object(top_trans_log, 'error')
    def test_logging_with_no_transactions(self, mock_error, mock_info, sample_data):
        """Тестирование логирования при отсутствии транзакций"""
        test_date = datetime(2023, 12, 1)
        top_trans(test_date, sample_data)

        mock_error.assert_called_once_with("За выбранный период нет трат")

    @patch.object(top_trans_log, 'info')
    def test_logging_with_valid_transactions(self, mock_info, sample_data):
        """Тестирование логирования при наличии транзакций"""
        test_date = datetime(2024, 1, 15)
        top_trans(test_date, sample_data)

        assert mock_info.call_count >= 3