from data_reader import data_reader

if __name__ == '__main__':
    dt = data_reader(2, 1, 'afd497b5-83e7-4ecf-8c98-cd1805aa16c9')
    dt.get_bus_data()
    dt.dump_data()
