import pandas as pd
import matplotlib.pyplot as plt


class data_visualizer:
    data_file_name: str
    bar_name: str
    xlabel_index: int
    ylabel_index: int

    def __init__(self, file_name, bar_name, x, y):
        self.data_file_name = file_name
        self.bar_name = bar_name
        self.xlabel_index = x
        self.ylabel_index = y

    def print_data(self):
        data = pd.read_csv(self.data_file_name, encoding='utf-16')
        data_headers = list(data.columns)
        print(data)
        fig, ax = plt.subplots()
        ax.bar(data[data_headers[self.xlabel_index]], data[data_headers[self.ylabel_index]])
        fig.subplots_adjust(bottom=0.3)
        plt.title(self.bar_name)
        plt.xlabel(data_headers[self.xlabel_index])
        plt.ylabel(data_headers[self.ylabel_index])
        plt.xticks(rotation=30, ha='right')

        plt.show()

