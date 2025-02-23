import os
import pandas as pd
from logconfig import logger
from pandas.errors import ParserError, EmptyDataError

class FileReader:
    def __init__(self, path="CSE-CIC-IDS2018"):
        self.__path_to_files = path

    def read_training_file(self, file_name):
        name = "8. Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"

        if not (name == file_name):
            try:    
                data = pd.read_csv(os.path.join(self.__path_to_files, file_name), header=0)
            except ParserError as e:
                logger.error(f"Parsing error: {e}")
            except EmptyDataError as e:
                logger.error(f"Empty file error: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
        else:
            data = pd.DataFrame()
    
        return data

    def read_training_files(self):
        files_and_dirs = os.listdir(self.__path_to_files)
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(self.__path_to_files, f))]

        dataframe = pd.DataFrame()
        for i in range(len(files)):
            data = self.read_training_file(files[i])
            if not data.empty:    
                dataframe = pd.concat([data, dataframe])

        return dataframe
