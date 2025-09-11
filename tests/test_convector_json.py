import pytest
import json
from unittest.mock import patch, mock_open
from src.utils import convector_json, convector_json_log


class TestConvectorJson:
    """Тесты для функции конвертации JSON файла"""

    def test_convector_json_success(self):
        """Тестирование успешной конвертации JSON файла"""
        test_data = [{"key": "value"}, {"number": 123}]

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            result = convector_json("test_file.json")

        assert result == test_data

    def test_convector_json_empty_file(self):
        """Тестирование пустого файла"""
        with patch("builtins.open", mock_open(read_data="")):
            result = convector_json("test_file.json")

        assert result == ["Файл пустой! Или не содержит .json"]

    def test_convector_json_file_not_found(self):
        """Тестирование когда файл не найден"""
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result = convector_json("nonexistent_file.json")

        assert result == ["Файл не найден"]

    def test_convector_json_unicode_error(self):
        """Тестирование ошибки кодировки"""
        with patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid")):
            result = convector_json("test_file.json")

        assert result == ["Не правильный формат файла"]

    @patch.object(convector_json_log, 'info')
    def test_convector_json_logging_success(self, mock_info):
        """Тестирование логирования при успешной конвертации"""
        test_data = [{"test": "data"}]

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            convector_json("test_file.json")

        assert mock_info.call_count >= 3

    @patch.object(convector_json_log, 'error')
    def test_convector_json_logging_error(self, mock_error):
        """Тестирование логирования при ошибке"""
        with patch("builtins.open", side_effect=FileNotFoundError()):
            convector_json("nonexistent_file.json")

        mock_error.assert_called_with("Файл не найден")