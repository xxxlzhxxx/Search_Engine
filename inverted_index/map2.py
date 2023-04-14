#!/usr/bin/env python3
"""Map 2."""
import sys
from utils import clean_query

def main():
    # Input comes from standard input
    for line in sys.stdin:
        term, IDF, doc_id_list, tf_list = line.strip().split('\t')
        IDF = float(IDF)
        doc_id_list = doc_id_list.strip('[]').split(', ')
        doc_id_list = [int(doc_id) for doc_id in doc_id_list]
        tf_list = tf_list.strip('[]').split(', ')
        tf_list = [int(tf) for tf in tf_list]
        for doc_id, tf in zip(doc_id_list, tf_list):
            print(f"{doc_id}\t{term}\t{IDF}\t{tf}")

if __name__ == "__main__":
    main()
