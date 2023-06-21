import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt    
import json
import os

def question1(data):
    plt.figure(figsize=(8, 6))
    sns.histplot(data=data, x='Title', weights='Rating', bins='auto')
    plt.title('Year vs Book Rating')
    plt.xlabel('Year')
    plt.ylabel('Book Rating')
    plt.savefig('artifacts/question1.png')  # Save the plot as an image
    plt.close()

def question2(data):
    avg_ratings = data.groupby('Publisher')['Rating'].mean().sort_values(ascending=False)[:10]
    print("These are the top 10 publishers with the highest average rating:")
    for i, publisher in enumerate(avg_ratings.index, start=1):
        print(f'{i}. {publisher}: {avg_ratings[publisher]:.2f}')

    plt.figure(figsize=(8, 6))
    sns.barplot(x=avg_ratings.values, y=avg_ratings.index, palette='viridis')
    plt.xlabel("Average Rating")
    plt.ylabel("Publisher")
    plt.title("Top 10 Publishers with Highest Average Rating")
    plt.savefig('artifacts/question2.png')  # Save the plot as an image
    plt.close()

def question3(data):
    book_ratings = data.groupby('Title')['Rating'].mean().sort_values(ascending=False)[:10]
    print("These are the top 10 books with the highest average rating:")
    for i, book_title in enumerate(book_ratings.index, start=1):
        print(f'{i}. {book_title}: {book_ratings[book_title]:.2f}')

    plt.figure(figsize=(8, 6))
    sns.barplot(x=book_ratings.values, y=book_ratings.index, palette='viridis')
    plt.xlabel("Book Rating")
    plt.ylabel("Books")
    plt.title("Top 10 Books with Highest Average Rating")
    plt.savefig('artifacts/question3.png')  # Save the plot as an image
    plt.close()

def question4(data):
    author_ratings = data.groupby('Author')['Rating'].mean().sort_values(ascending=False)[:10]
    print("These are the top 10 authors with the highest average rating:")
    for i, book_author in enumerate(author_ratings.index, start=1):
        print(f'{i}. {book_author}: {author_ratings[book_author]:.2f}')

    plt.figure(figsize=(8, 6))
    sns.barplot(x=author_ratings.values, y=author_ratings.index, palette='viridis')
    plt.xlabel("Author Rating")
    plt.ylabel("Author Name")
    plt.title("Top 10 Authors with Highest Average Rating")
    plt.savefig('artifacts/question4.png')  # Save the plot as an image
    plt.close()

if __name__ == "__main__":
    # Read the data from the CSV file
    data = pd.read_csv('/Users/tarakram/Documents/Recommendation-Project/data/processed/pre-processed_data.csv')

    # Drop the 'Unnamed: 0' column if present
    data.drop('Unnamed: 0', axis=1, inplace=True)

    # Convert column names to lowercase
    data['Title'] = data['Book-Title']
    data['Author'] = data['Book-Author']
    data['Rating'] = data['Book-Rating']
    data['Publisher'] = data['Publisher']

    # Call the functions
    question1(data)
    question2(data)
    question3(data)
    question4(data)

    # Create the JSON response
    response = {
        'question1': {
            'plot': 'question1.png',
            'data': data['Title'].tolist()
        },
        'question2': {
            'plot': 'question2.png',
            'data': data.groupby('Publisher')['Rating'].mean().sort_values(ascending=False)[:10].to_dict()
        },
        'question3': {
            'plot': 'question3.png',
            'data': data.groupby('Title')['Rating'].mean().sort_values(ascending=False)[:10].to_dict()
        },
        'question4': {
            'plot': 'question4.png',
            'data': data.groupby('Author')['Rating'].mean().sort_values(ascending=False)[:10].to_dict()
        }
    }

    # Save JSON response to file
    json_path = 'artifacts/eda.json'
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w') as json_file:
        json.dump(response, json_file)
