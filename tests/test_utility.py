import pytest

from warsawbuspy.utility.data_utility import time_parser, assert_file_extension, is_location_valid
from warsawbuspy.utility.exceptions import InvalidFileExtensionException


class TestUtility:
    def test_time_parser(self):
        assert time_parser('24:00:00') == '00:00:00'
        assert time_parser('25:00:00') == '01:00:00'
        assert time_parser('26:00:00') == '02:00:00'
        assert time_parser('27:00:00') == '03:00:00'
        assert time_parser('28:00:00') == '04:00:00'
        assert time_parser('29:00:00') == '05:00:00'
        assert time_parser('15:23:32') == '15:23:32'

    def test_file_extension_assertion_without_exception(self):
        assert_file_extension('uabuga.sda', '.sda')

    def test_file_extension_assertion_for_length(self):
        with pytest.raises(InvalidFileExtensionException) as e_info:
            assert_file_extension('sda', '.sda')

    def test_file_extension_assertion_invalid_extention(self):
        with pytest.raises(InvalidFileExtensionException) as e_info:
            assert_file_extension('ugabuba.json', '.csv')

    def test_location_validity(self):
        assert is_location_valid(21.00, 54.00) is True
        assert is_location_valid(21.00, 91.00) is False
        assert is_location_valid(-10.00, 54.00) is True
        assert is_location_valid(-200.00, 54.00) is False
        assert is_location_valid(300.00, -1000.00) is False
