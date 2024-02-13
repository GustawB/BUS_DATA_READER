import pandas as pd
import matplotlib.pyplot as plt


class DataVisualizer:
    @staticmethod
    def print_data(data_file_name, bar_name, first_data_to_draw, size_of_data_to_draw):
        data = pd.read_csv(data_file_name, encoding='utf-16')
        data_headers = list(data.columns)
        data = data[first_data_to_draw:first_data_to_draw + size_of_data_to_draw]
        fig, ax = plt.subplots()
        ax.bar(data[data_headers[0]].astype(str), data[data_headers[1]].astype(int))
        fig.subplots_adjust(bottom=0.3)
        plt.title(bar_name)
        plt.xlabel(data_headers[0])
        plt.ylabel(data_headers[1])
        plt.xticks(rotation=30, ha='right')

        plt.show()

