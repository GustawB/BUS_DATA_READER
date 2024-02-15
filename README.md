# Bus data reader

This package represents the functionality of reading and analyzing data from https://api.um.warszawa.pl/#.

## Instalation:
This package can be installed by calling:
```
pip install warsawbuspy
```

## Contents:
This package contains three subpackages:
### 1. readers:
This subpackage contains a data_readers module, in which DataReader class is stored, that contains the functionality of
reading a various data from the API as well as writing it into the .csv files.

### 2. analyzers:
This subpackage contains two modules:
- data_analyzer: this module contains the DataAnalyzer class that contains the functionality of retrieving
    data fetched by the DataReader class from the .csv files as well as functionality of analyzing it. This class
    also contains the functionality of storing results of the analysis into the .csv files.
- data_visualizer: this module contains the DataVisualizer class, that contains the functionality of 
    representing the results of the analysis as charts.

### 3. holders:
This subpackage contains the module data_holders, in which are stored all classes used to store data 
throughout the project.

## APIs:
This project utilizes two APIs:
- https://api.um.warszawa.pl: from here, all the data related to the city communication is fetched (bus locations,
  schedules etc.)
- https://services.gugik.gov.pl: from here, the data about the street name for the given coordinates is fetched.
