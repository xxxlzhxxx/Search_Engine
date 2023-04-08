"""index api."""
import math
import pathlib
import re
import flask
import index
import os


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
    index.app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    

def read_pagerank():
    with open ('index_server/index/pagerank.out') as file:
        
    

def read_stopwords():
    pass

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
    hits = []


def get_page():
    pass


def get_hits():
    pass

