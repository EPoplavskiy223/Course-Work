import pytest
from unittest.mock import patch, mock_open
from src.reports import save_report


class TestSaveReport:

    def test_save_report_with_default_filename(self):
        @save_report()
        def test_function():
            return "test result"

        with patch('builtins.open', mock_open()) as mock_file:
            result = test_function()

            assert result == "test result"
            mock_file.assert_called_once()
            mock_file().write.assert_called_once_with("test result")

    def test_save_report_with_custom_filename(self):
        @save_report("custom_report.txt")
        def test_function():
            return "test result"

        with patch('builtins.open', mock_open()) as mock_file:
            result = test_function()

            assert result == "test result"
            mock_file.assert_called_once_with("custom_report.txt", "w", encoding="utf-8")
            mock_file().write.assert_called_once_with("test result")

    def test_save_report_preserves_original_function(self):
        @save_report()
        def test_function(x, y=10):
            return x + y

        result = test_function(5, y=3)

        assert result == 8