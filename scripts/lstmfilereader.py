from logconfig import logger
import pandas as pd
import os
from filereader import FileReader 
from pandas.errors import ParserError, EmptyDataError

class LstmFileReader(FileReader):
    def __init__(self, path):
        super().__init__(path)
        self.__path_to_files = path

    def read_training_file(self, file_name):
        whitelist = [
            "1. Monday-WorkingHours.pcap_ISCX.csv",
            "2. Tuesday-WorkingHours.pcap_ISCX.csv"
        ]

        if not (file_name in whitelist):
            print("wrong file")
            data = pd.DataFrame()
        else:
            try:
                data = pd.read_csv(os.path.join(self.__path_to_files, file_name), header=0)
            except ParserError as e:
                logger.error(f"Parsing error: {e}")
            except EmptyDataError as e:
                logger.error(f"Empty file error: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
    
        return data
    
    def read_test_file(self):
        file_name = "3. Wednesday-workingHours.pcap_ISCX.csv"

        try:
            data = pd.read_csv(os.path.join(self.__path_to_files, file_name), header=0)
        except ParserError as e:
            logger.error(f"Parsing error: {e}")
        except EmptyDataError as e:
            logger.error(f"Empty file error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
    
        return data
    
    def read_training_files(self):
        files_and_dirs = os.listdir(self.__path_to_files)
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(self.__path_to_files, f))]
        files.sort()

        dataframe = pd.DataFrame()
        for i in range(2):
            data = self.read_training_file(files[i])
            if not data.empty:
                dataframe = pd.concat([data, dataframe])
        return dataframe