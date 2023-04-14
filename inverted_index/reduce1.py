#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
from math import log10 as log
from collections import defaultdict


def reduce_one_group(key, group):
    """Reduce one group."""
    #  (term, doc_id)
    doc_with_term = defaultdict(int)
    for content in group:
        # remove \n
        content = content[:-1]
        doc_id = int(content.split("\t")[1])
        doc_with_term[doc_id] += 1
    doc_tf_list = []
    doc_id_list = []
    for doc_id, tf in doc_with_term.items():
        doc_tf_list.append(tf)
        doc_id_list.append(doc_id)
    with open("output0/part-00000") as f:
        N = int(f.read())
    df = len(doc_with_term)
    print(f"{key}\t{log(N/df)}\t{doc_id_list}\t{doc_tf_list}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()