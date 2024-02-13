# Bus data reader

This package represents the functionality of reading and analyzing data from https://api.um.warszawa.pl/#. The package contains three subpackages:

    1. data_holders: this package contains all classes that holds data read from the API.

    2. readers: this package contains all the functionality of calling the API for data, and then dumping the data into
       the .csv files.

    3. analyzers: this package contains all the functionality of analyzing the collected data, as well as displaying it using
       the matplotlib. 
