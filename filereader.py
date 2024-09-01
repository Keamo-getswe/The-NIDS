import os
import pandas as pd
from utility import NO_OF_FEATURES
import os

class FileReader:
    def __init__(self, path):
        self.__path_to_files = path

    def read_file(self, file_name):
        extension = ".csv"

        if extension in file_name:
            data = pd.read_csv(os.path.join(self.__path_to_files, file_name), header=0)
    
        return data

    def read_files(self):
        files_and_dirs = os.listdir(self.__path_to_files)
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(self.__path_to_files, f))]

        dataframe = pd.DataFrame()
        for i in range(len(files)):
            data = self.read_file(files[i])
            dataframe = pd.concat([data, dataframe])

        return dataframe
