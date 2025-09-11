import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch
from src.reports import spending_by_category


class TestSpendingByCategory:

    @pytest.fixture
    def sample_transactions(self):
        today = datetime.now()
        return pd.DataFrame({
            "Дата операции": [
                (today - timedelta(days=10)).strftime("%d.%m.%Y %H:%M:%S"),
                (today - timedelta(days=20)).strftime("%d.%m.%Y %H:%M:%S"),
                (today - timedelta(days=30)).strftime("%d.%m.%Y %H:%M:%S"),
                (today - timedelta(days=40)).strftime("%d.%m.%Y %H:%M:%S")
            ],
            "Категория": ["Еда", "Еда", "Транспорт", "Еда"],
            "Сумма операции": [-1000.50, -1500.00, -500.75, -2000.00]
        })

    def test_spending_by_category_with_date(self, sample_transactions):
        today = datetime.now().strftime("%d.%m.%Y")
        result = spending_by_category(sample_transactions, "Еда", today)

        assert len(result) == 3
        assert all(result["Категория"] == "Еда")
        assert all(result["Сумма операции"] < 0)

    def test_spending_by_category_without_date(self, sample_transactions):
        result = spending_by_category(sample_transactions, "Еда")

        assert len(result) == 3
        assert all(result["Категория"] == "Еда")

    def test_spending_by_category_no_results(self, sample_transactions):
        result = spending_by_category(sample_transactions, "Развлечения")

        assert len(result) == 0

    def test_spending_by_category_different_category(self, sample_transactions):
        result = spending_by_category(sample_transactions, "Транспорт")

        assert len(result) == 1
        assert result.iloc[0]["Категория"] == "Транспорт"

    def test_spending_by_category_positive_transactions(self):
        today = datetime.now()
        transactions_with_positive = pd.DataFrame({
            "Дата операции": [
                (today - timedelta(days=10)).strftime("%d.%m.%Y %H:%M:%S"),
                (today - timedelta(days=20)).strftime("%d.%m.%Y %H:%M:%S")
            ],
            "Категория": ["Еда", "Еда"],
            "Сумма операции": [1000.50, -1500.00]
        })

        result = spending_by_category(transactions_with_positive, "Еда")

        assert len(result) == 1
        assert result.iloc[0]["Сумма операции"] == -1500.00