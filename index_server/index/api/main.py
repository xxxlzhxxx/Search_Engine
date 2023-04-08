"""index api."""
import math
import pathlib
import re
import flask
import index
import os
from pathlib import Path


def init():
    """Load the relavent files into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    global pagerank
    pagerank = {}
    global stopwords
    stopwords = set()
    global inverted
    inverted = {}
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
            num_docs = (len(line)-2)// 3
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
    with open('index_server/index/pagerank.out') as file:
        for line in file:
            doc_id, rank = line.strip().split(',')
            pagerank[doc_id] = float(rank)


def read_stopwords():
    """Read stopwords."""
    with open("index_server/index/stopwords.txt", 'r', encoding="utf-8") as file:
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
def doc_ID_score():
    """Show hits."""
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w')
    query = query_clean(query)
    hits = search_result(query)
    context = {
        "hits": hits,
    }
    return flask.jsonify(**context)


def query_clean(query):
    """Clean query."""
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold()
    query = query.split()
    query = [word for word in query if word not in index.stopwords]
    result = {}
    for term in query:
        if term in result:
            result[term] += 1
        else:
            result[term] = 1
    return result

def search_result(query):
    pass