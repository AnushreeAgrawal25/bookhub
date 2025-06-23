#google API search end point

import requests

def search_google_books(query: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch books from Google API"}
    
    data = response.json()
    books = []

    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        books.append({
            "title": volume_info.get("title"),
            "authors": volume_info.get("authors", []),
            "publishedDate": volume_info.get("publishedDate", "N/A")
        })

    return books

