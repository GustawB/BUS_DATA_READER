import csv
import os

import pytest

from warsawbuspy.analyzers.data_comparator import DataComparator


class TestDataComparatorClass:
    @staticmethod
    def generate_data(test_file_name, data_keys, data_values):
        column_names = ['Street_name', 'BLBL']
        assert len(data_keys) == len(data_values)
        with open(test_file_name, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(column_names)
            for i in range(len(data_keys)):
                row = [data_keys[i], data_values[i]]
                csv_writer.writerow(row)

    @pytest.fixture
    def expected_data_diff(self):
        return {
            'A': 10.0,
            'B': 0.0,
            'C': 10.5,
            'D': 10.38,
            'E': 17.17
        }

    def test_data_comparation(self, expected_data_diff):
        if not os.path.isdir('test_files'):
            os.mkdir('test_files')
        self.generate_data('test_files/test_data_1.csv', ['A', 'B', 'C', 'D', 'E'],
                           ['90', '80', '70.5', '69.75', '21.37'])
        self.generate_data('test_files/test_data_2.csv', ['A', 'B', 'C', 'D', 'E'],
                           ['80', '80', '60', '59.37', '4.2'])
        dc = DataComparator()
        dc.comp_data('test_files/test_data_1.csv', 'test_files/test_data_2.csv')
        data_dict = dc.data_comp_result
        assert data_dict == expected_data_diff
        dc.dump_data_comp_result('test_files/test_data_comp_result.csv', ['Street_name', 'LBLB'])


