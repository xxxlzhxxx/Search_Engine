from threading import Thread
import flask
import search
import requests

def my_function(url, query, weight, results, idx):
    """Searches a URL with a given query and weight."""
    full_url = f"{url}?q={query}&w={weight}"
    try:
        response = requests.get(full_url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error searching index: {err}")
    else:
        results[idx] = response.json()


@search.app.route("/", methods=["GET"])
def show_index():
    """Display / route."""
    connection = search.model.get_db()
    context = {}
    context["docs"] = []
    context["num_docs"] = 0
    query = flask.request.args.get("q", type=str)
    weight = flask.request.args.get("w", type=float)
    if query is None:
        return flask.render_template("index.html", **context)
    threads = []
    results = [[] for _ in range(len(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]))]
    for index, url in enumerate(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]):
        thread = Thread(target=my_function, args=(url, query, weight, results, index))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    docs = []
    for result in results:
        if len(result) != 0:
            for doc in result["hits"]:
                docs.append(doc)
    docs.sort(key=lambda x: x["score"], reverse=True)
    if len(docs) > 10:
        docs = docs[:10]
    doc_info = []
    for doc in docs:
        cur = connection.execute(
            "SELECT title, summary, url FROM Documents WHERE docid = ?", (doc["docid"],)
        )
        doc_info.append(cur.fetchone())
    context["docs"] = doc_info
    context["num_docs"] = len(doc_info)
    
    return flask.render_template("index.html", **context)