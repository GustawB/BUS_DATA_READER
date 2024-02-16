import os.path

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import json


# Class responsible for displaying the results of the data analysis.
class DataVisualizer:
    # Function that draws a chart of a data in the given file. It takes the name of the file that we want to take
    # data from, name of the chart, and then the position of the first dat in the file that we want to represent,
    # and then the number of total data entries that we want to show. By default, the first column of the file
    # will represent the X axis of the chart, and the second one will represent the Y axis of the chart, but the
    # user can change that by specifying the x_axis_index and y_axis_index params (0 and 1 by default).
    @staticmethod
    def draw_data_chart(data_file_name, bar_name, first_data_to_draw, size_of_data_to_draw, x_axis_index=0,
                        y_axis_index=1):
        data = pd.read_csv(data_file_name, encoding='utf-16')
        data_headers = list(data.columns)
        data = data[first_data_to_draw:first_data_to_draw + size_of_data_to_draw]
        fig, ax = plt.subplots()
        ax.bar(data[data_headers[x_axis_index]].astype(str), data[data_headers[y_axis_index]].astype(int))
        fig.subplots_adjust(bottom=0.3)
        plt.title(bar_name)
        plt.xlabel(data_headers[0])
        plt.ylabel(data_headers[1])
        plt.xticks(rotation=30, ha='right')

        plt.show()

    # Function that draws the locations of the ovespeeding incidents on the Warsaw map. This map is fetched
    # from the API if the file warsaw_map.geojson doesn't exist.
    @staticmethod
    def draw_data_map(ovespeed_locations, title):
        if not os.path.isfile('warsaw_map.geojson'):
            response = requests.get('https://raw.githubusercontent.com/ppatrzyk/polska-geojson/master/powiaty/powiaty'
                                    '-medium.geojson')
            warsaw_map_coords = response.json()['features'][301]
            temp = response.json()['features'][301]
            data_to_write = json.dumps(temp, indent=4)
            with open('warsaw_map.geojson', 'w') as file:
                file.write(data_to_write)
        warsaw_map = gpd.read_file('warsaw_map.geojson')
        base = warsaw_map.plot(color='green', edgecolor='black')
        locations_data = gpd.read_file(ovespeed_locations)
        locations_data.plot(ax=base, color='red', markersize=15)
        plt.title(title)
        plt.show()
