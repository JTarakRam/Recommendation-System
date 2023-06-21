import os
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# Set up the project directory and add it to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

from config.config import ARTIFACTS_DIR
from config.config import logger
from ingestion import DataIngestion

class Recommender:
    def __init__(self):
        self.model_path = os.path.join(ARTIFACTS_DIR, 'recommendation_model.pkl')
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}. Please run 'model.py' first to build the model.")
        self.pivot_table, self.similarity_scores = self.load_model()
    
    def load_model(self):
        with open(self.model_path, 'rb') as file:
            pivot_table, similarity_scores = pickle.load(file)
        return pivot_table, similarity_scores
    
    def recommend(self):
        book_name = input("Enter the book name: ")

        # Check if book_name is present in pivot_table.index
        if book_name not in self.pivot_table.index:
            print(f"Book '{book_name}' not found in the dataset.")
            return

        index = np.where(self.pivot_table.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(self.similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:]

        num_recommendations = input("How many recommendations do you want? ")
        try:
            num_recommendations = int(num_recommendations)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        if num_recommendations <= 0:
            print("Number of recommendations should be greater than 0.")
            return

        recommendations = []
        for i, index in enumerate(similar_items, start=1):
            if i > num_recommendations:
                break
            book_title = self.pivot_table.index[index[0]]
            recommendations.append(book_title)
            print(f"{i}. {book_title}")
            print('--')

        if len(recommendations) == 0:
            print("No recommendations found.")

if __name__ == '__main__':
    recommender = Recommender()
    recommender.recommend()
