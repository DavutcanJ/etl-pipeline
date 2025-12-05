import pandas as pd
from typing import Dict

class ETLExtractor:    
    """
    ETL işlemleri için veri çıkarma fonksiyonlarını içerir.
    """
    
    @staticmethod
    def extract_data(file_path)-> Dict[str, pd.DataFrame]:

        """
        Extracts data from the given file path.

        Args:
            file_path (str): The path to the file from which to extract data.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        extracted_data = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    key, value = line.strip().split('=')
                    extracted_data[key] = value
        except Exception as e:
            print(f"An error occurred while extracting data: {e}")
        
        return extracted_data

