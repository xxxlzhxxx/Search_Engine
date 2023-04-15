#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
from collections import defaultdict


def reduce_one_group(group):
    """Reduce one group."""
    per_term_data = defaultdict(dict)
    per_term_idf = {}
    for content in group:
        # from map
        # print(f"{doc_id%3}\t{term}\t{idf}\t{doc_id}\t{tf}\t{norm_fact}")
        _, term, idf, doc_id, freq, norm_fact = content.strip().split("\t")
        per_term_idf[term] = idf
        per_term_data[term][doc_id] = (freq, norm_fact)
    # ascending order
    term_orders = sorted(per_term_data.keys())
    for term in term_orders:
        term_data = per_term_data[term]
        doc_orders = sorted(term_data.keys())
        print(f"{term} {per_term_idf[term]}", end="")
        for doc_id in doc_orders:
            freq, norm_fact = term_data[doc_id]
            print(f" {doc_id} {freq} {norm_fact}", end="")
        print()


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
