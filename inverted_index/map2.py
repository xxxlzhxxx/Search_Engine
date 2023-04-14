#!/usr/bin/env python3
"""Map 2."""
import sys


def main():
    """Map 2."""
    for line in sys.stdin:
        term, idf, doc_id_list, tf_list = line.strip().split("\t")
        idf = float(idf)
        doc_id_list = doc_id_list.strip("[]").split(", ")
        doc_id_list = [int(doc_id) for doc_id in doc_id_list]
        tf_list = tf_list.strip("[]").split(", ")
        tf_list = [int(tf) for tf in tf_list]
        for doc_id, freq in zip(doc_id_list, tf_list):
            print(f"{doc_id}\t{term}\t{idf}\t{freq}")


if __name__ == "__main__":
    main()
