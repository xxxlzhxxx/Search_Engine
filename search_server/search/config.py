"""Configuration for the search server."""
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = 'var/search.sqlite3'
