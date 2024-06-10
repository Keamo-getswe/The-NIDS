from filereader import FileReader
from preprocessor import Preprocessor
import os

class Agent:
    def __init__(self, path):
        self.__reader = FileReader(path)
        self.__preprocessor = Preprocessor()
        self.__data = None
        self.__labels = None

    def getData(self):
        return self.__data
    
    def getLabels(self):
        return self.__labels

    def set_data_from_files(self):
        self.__data, self.__labels = self.__reader.read_files()

    def enumerate_labels(self):
        temp = self.__labels
        self.__labels = self.__labels.apply(lambda x: 0 if x == 'BENIGN' else 1)

    def preprocess(self):
        self.set_data_from_files()
        self.enumerate_labels()

        return self.__preprocessor.process_data(self.__data)