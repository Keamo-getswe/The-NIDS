from filereader import FileReader
from preprocessor import Preprocessor

class Agent:
    def __init__(self, path):
        self.__reader = FileReader(path)
        self.__preprocessor = Preprocessor()

    def set_data_from_files(self):
        return self.__reader.read_files()

    def preprocess(self):
        data = self.set_data_from_files()
        train_data, train_labels, test_data, test_labels = self.__preprocessor.process_data(data)

        return train_data, train_labels, test_data, test_labels