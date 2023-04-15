"""index api."""
import math
import re
from pathlib import Path
import os
import index
import flask


pagerank = {}
inverted = {}
stopwords = set()


def init():
    """Load the relavent files into memory."""
    read_inverted()
    read_pagerank()
    read_stopwords()


def read_inverted():
    """Read inverted index."""
    index.app.config["INDEX_PATH"] = os.getenv(
        "INDEX_PATH", "inverted_index_1.txt"
    )
    path_dir = "index_server/index/inverted_index"
    with open(Path(path_dir) / Path(index.app.config['INDEX_PATH']),
              'r',
              encoding='UTF-8') as file:
        for line in file:
            line = line.split()
            term = line[0]
            idf = line[1]
            num_docs = (len(line)-2) // 3
            inverted[term] = {}
            inverted[term]['idf'] = float(idf)
            inverted[term]['docs'] = {}
            for i in range(num_docs):
                doc_id = line[3 * i + 2]
                term_frequency = line[3 * i + 3]
                norm_factor = line[3 * i + 4]
                inverted[term]["docs"][doc_id] = {
                    "tf": term_frequency,
                    "norm_factor": norm_factor,
                }


def read_pagerank():
    """Read pagerank."""
    with open('index_server/index/pagerank.out', encoding="utf-8") as file:
        for line in file:
            doc_id, rank = line.strip().split(',')
            pagerank[doc_id] = float(rank)


def read_stopwords():
    """Read stopwords."""
    file_path = Path("index_server/index/stopwords.txt")
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            stopwords.add(line.strip())


@index.app.route('/api/v1/', methods=['GET'])
def service_list():
    """Display the service list."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=["GET"])
def doc_score():
    """Show hits."""
    query = flask.request.args.get("q", default="", type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)
    query = query_clean(query)
    hits = search_result(query, weight)
    context = {
        "hits": hits,
    }
    return flask.jsonify(**context)


def query_clean(query):
    """Clean query."""
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold()
    query = query.split()
    query = [word for word in query if word not in stopwords]
    result = {}
    for term in query:
        if term in result:
            result[term] += 1
        else:
            result[term] = 1
    return result


def square_generator(vector):
    """Func gen."""
    for vec in vector:
        yield vec*vec


def dot_product_generator(vector1, vector2):
    """Func generator."""
    for vec1, vec2 in zip(vector1, vector2):
        yield vec1 * vec2


def search_result(query, weight):
    """Search a query."""
    # build the query vector
    pterm = list(query.keys())[0]
    doc_ids = set(inverted[pterm]["docs"].keys())
    # Get all documents that contain all the terms in query
    for term in query:
        if term not in inverted:
            return []
        doc_ids = doc_ids.intersection(
            set(inverted[term]["docs"].keys())
        )

    results = []
    for doc_id in doc_ids:
        query_vector = []
        document_vector = []
        norm_d_squared = 0
        for term in query:
            # Calculate query vector
            term_frequency = query[term]
            idf = inverted[term]["idf"]
            query_vector.append(term_frequency * idf)
            # Calculate document vector
            term_frequency = int(
                inverted[term]["docs"][doc_id]["tf"]
            )
            idf = inverted[term]["idf"]
            document_vector.append(term_frequency * idf)
            # Calculate norm_d_squared
            norm_d_squared = (
                inverted[term]["docs"][doc_id]["norm_factor"]
            )

        # Calculate cosine similarity
        tfidf = sum(dot_product_generator(query_vector, document_vector)) / \
            (math.sqrt(sum(square_generator(query_vector))) *
                math.sqrt(float(norm_d_squared)))
        page_rankk = pagerank[doc_id]
        weighted_score = weight * page_rankk + (1 - weight) * tfidf
        results.append({
            "docid": int(doc_id),
            "score": weighted_score,
        })
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
