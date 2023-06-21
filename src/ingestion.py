import pandas as pd
import numpy as np
from pathlib import Path
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from config.config import logger

import warnings
warnings.filterwarnings('ignore')


class DataIngestion:
    @staticmethod
    def load_data():
        books_data = pd.read_csv('data/raw/Books.csv')
        ratings_data = pd.read_csv('data/raw/Ratings.csv')
        users_data = pd.read_csv('data/raw/Users.csv')
        logger.info('Data Loaded')
        return books_data, ratings_data, users_data
    
    @staticmethod
    def ingest():
        # Load the data
        books_data, ratings_data, users_data = DataIngestion.load_data()

        # Merge books_data and ratings_data on 'ISBN'
        merged_data = books_data.merge(ratings_data, on='ISBN')
        print(merged_data.head())

        # Merge ratings_data and users_data on 'Book-Title'
        final_data = merged_data.merge(users_data, on='User-ID')
        final_data.to_csv('/Users/tarakram/Documents/Recommedation-System/data/processed/Ingested_data.csv')
        print(final_data.head())
        print(final_data.columns)
        logger.info('Ingested the data!')

        return final_data
    
if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.load_data()
    data_ingestion.ingest()  