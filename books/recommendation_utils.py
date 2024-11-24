from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from .models import Book

def get_book_recommendations(book_id, top_n=5):
    # Fetch all books
    books = Book.objects.all()

    # Create a DataFrame with necessary fields
    data = []
    for book in books:
        genres = " ".join([genre.name for genre in book.genre.all()])
        data.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category.name,
            "genres": genres,
            "description": book.description or ""
        })
    books_df = pd.DataFrame(data)

    # Combine metadata for TF-IDF processing
    books_df['metadata'] = books_df['genres'] + " " + books_df['category'] + " " + books_df['description']

    # Initialize TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(books_df['metadata'])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find the index of the input book
    book_idx = books_df.index[books_df['id'] == book_id].tolist()[0]

    # Get similarity scores for the input book
    similarity_scores = list(enumerate(cosine_sim[book_idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Fetch the top N similar books (excluding the input book itself)
    similar_books_indices = [i[0] for i in similarity_scores[1:top_n + 1]]
    recommended_books = books_df.iloc[similar_books_indices]

    # Return recommended books as a list of dicts
    return recommended_books[['id', 'title', 'author']].to_dict('records')
