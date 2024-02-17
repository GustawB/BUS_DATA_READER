import csv


class DataComparator:
    __slots__ = ('__data_1', '__data_2', '__data_comp_result',)

    def __init__(self):
        self.__data_1 = {}
        self.__data_2 = {}
        self.__data_comp_result = {}

    @property
    def data_comp_result(self) -> dict:
        return self.__data_comp_result

    # Utility function to read data from the given file to the given data holder (one of the DataComparator
    # fields). This function treats the first column of the file as keys, and the second one as values.
    @staticmethod
    def __read_data_from_file(file_to_read_from: str, data_holder: dict) -> None:
        with open(file_to_read_from, 'r', encoding='utf16') as file:
            csv_reader = csv.reader(file)
            row_nr = 1
            for row in csv_reader:
                row_nr += 1
                if row_nr > 0:
                    data_holder[row[0]] = row[1]

    # Utility function to store the results of the comparison into the given file with the given column names.
    def __write_data_to_file(self, file_to_write_into: str, column_names: list) -> None:
        with open(file_to_write_into, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(column_names)
            for key in self.__data_comp_result:
                row = [key, self.__data_comp_result[key]]
                csv_writer.writerow(row)

    # Function that compares the differences between data in two files for every data key
    # that appears IN BOTH files. Both files should represent the data of the same type.
    def comp_data(self, file_to_read_1: str, file_to_read_2: str) -> None:
        self.__read_data_from_file(file_to_read_1, self.__data_1, )
        self.__read_data_from_file(file_to_read_2, self.__data_2)
        nr_of_lines = 0
        for key in self.__data_1:
            nr_of_lines += 1
            if nr_of_lines > 1 and key in self.__data_2:
                self.__data_comp_result[key] = round(float(self.__data_1[key]) - float(self.__data_2[key]), 3)

    # Function that dumps the result of the data comparison into the given file with the given
    # column names (passed as list). This operation deletes data in __data_1, __data_2 and __data_comp_result.
    def dump_data_comp_result(self, file_to_dump: str, column_names: list) -> None:
        self.__write_data_to_file(file_to_dump, column_names)
        self.__data_1.clear()
        self.__data_2.clear()
        self.__data_comp_result.clear()
