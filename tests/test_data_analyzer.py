from data_analyzer import data_analyzer


class TestDataAnalyzerClass:
    def test_nr_of_overspeeding_busses(self):
        da = data_analyzer()
        da.read_bus_data('test_files/test_bus_data.csv')
        assert da.calc_nr_of_overspeeding_busses() == 3
        assert da.nr_of_invalid_speeds == 1
        assert da.nr_of_invalid_times == 0