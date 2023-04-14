#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(group):
    """Reduce one group."""
    #  (term, doc_id)
    norm_factor_squared = 0
    term_data = []
    for content in group:
        # remove \n
        content = content[:-1]
        doc_id, term, idf, freq = content.split("\t")
        term_data.append((doc_id, term, idf, freq))
        norm_factor_squared += (float(freq) * float(idf)) ** 2
    for doc_id, term, idf, freq in term_data:
        print(f"{doc_id}\t{term}\t{idf}\t{freq}\t{norm_factor_squared}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
