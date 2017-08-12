import pandas


class CSVClient(object):
    def __init__(self, **kwargs):
        self._filename = kwargs.get('filename')

    def read(self):
        dataframe = pandas.read_csv(self._filename)
        return dataframe
   
