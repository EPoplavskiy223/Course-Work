import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.utils import reading_excel_file, excel_log


class TestReadingExcelFile:
    """Тесты для функции чтения excel файла"""

    @patch('pandas.read_excel')
    def test_reading_excel_file_success(self, mock_read_excel):
        """Тестирование успешного чтения excel файла"""
        # Мокируем данные
        mock_data = {
            'Номер карты': ['1234', '5678'],
            'Сумма операции': [1000, 2000],
            'Категория': ['Еда', 'Транспорт']
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_excel.return_value = mock_df

        result = reading_excel_file('test_file.xlsx')

        assert len(result) == 2
        assert result[0]['Номер карты'] == '1234'
        assert result[1]['Категория'] == 'Транспорт'

    @patch('pandas.read_excel')
    def test_reading_excel_file_with_none_values(self, mock_read_excel):
        """Тестирование чтения файла с None значениями"""
        # Мокируем данные с NaN
        mock_data = {
            'Номер карты': ['1234', None],
            'Сумма операции': [1000, 2000]
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_excel.return_value = mock_df

        result = reading_excel_file('test_file.xlsx')

        assert result[0]['Номер карты'] == '1234'
        assert result[1]['Номер карты'] is None

    @patch('pandas.read_excel')
    def test_reading_excel_file_unicode_error(self, mock_read_excel):
        """Тестирование ошибки чтения файла"""
        mock_read_excel.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'Invalid byte')

        result = reading_excel_file('test_file.xlsx')

        assert result == "Ошибка! Файл не читается"

    @patch.object(excel_log, 'info')
    @patch('pandas.read_excel')
    def test_reading_excel_file_logging_success(self, mock_read_excel, mock_info):
        """Тестирование логирования при успешном чтении"""
        mock_df = pd.DataFrame({'test': [1, 2]})
        mock_read_excel.return_value = mock_df

        reading_excel_file('test_file.xlsx')

        mock_info.assert_called_with("Файл успешно прочитан и конвертирован")

    @patch.object(excel_log, 'error')
    @patch('pandas.read_excel')
    def test_reading_excel_file_logging_error(self, mock_read_excel, mock_error):
        """Тестирование логирования при ошибке чтения"""
        mock_read_excel.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'Invalid byte')

        reading_excel_file('test_file.xlsx')

        mock_error.assert_called_with("ошибка в чтении файла")