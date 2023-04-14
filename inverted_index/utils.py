import re

with open("stopwords.txt") as f:
    stopwords = f.read().splitlines()

def clean_query(query) -> list:
    query = query.split(",")
    query = [q.strip('"') for q in query]
    title = query[1]
    body = query[2]
    whole = title + " " + body
    whole = re.sub(r"[^a-zA-Z0-9 ]+", "", whole)
    whole = whole.casefold()
    tokens = whole.split()
    tokens_without_stopwords = [word for word in tokens if not word in stopwords]
    return int(query[0]), tokens_without_stopwords