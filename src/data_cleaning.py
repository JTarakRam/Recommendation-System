from pathlib import Path
import pickle
import numpy as np
import pandas as pd
import os
import warnings
import sys
warnings.filterwarnings("ignore")
from ingestion import DataIngestion

data_ingestion = DataIngestion()
books_data, ratings_data, users_data = data_ingestion.load_data()

class PreProcessor:
    @staticmethod
    def clean_data():
        # Merge books_data and ratings_data on 'ISBN'
        merged_data = books_data.merge(ratings_data, on='ISBN')

        # Merge ratings_data and users_data on 'User-ID'
        final_data = merged_data.merge(users_data, on='User-ID')

        # Select only the desired columns
        desired_columns = ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication',
                           'Publisher', 'User-ID', 'Age', 'Book-Rating','Image-URL-L']
        final_data = final_data[desired_columns]

        # Perform cleaning operations on the final_data DataFrame
        final_data = final_data.drop_duplicates()
        print(final_data)
        print(final_data.shape)
        # Handle outliers and missing values in 'Age'
        Q1 = final_data['Age'].quantile(0.25)
        Q3 = final_data['Age'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        lower_bound = Q1 - 1.5 * IQR
        
        final_data = final_data[(final_data['Age'] >= lower_bound) & (final_data['Age'] <= upper_bound)]
        
        print(final_data)
        print(final_data.shape)
        print(final_data.columns)

        # Save cleaned data to a file
        processed_data_path = '/Users/tarakram/Documents/Recommendation-Project/data/processed/pre-processed_data.csv'
        final_data.to_csv(processed_data_path)
        # logger.info('Cleaned data saved at {}'.format(processed_data_path))

if __name__ == "__main__":
    preprocessor = PreProcessor()
    preprocessor.clean_data()


