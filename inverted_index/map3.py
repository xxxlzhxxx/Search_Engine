#!/usr/bin/env python3
"""Map 3."""
import sys


def main():
    """Map 3."""
    # Input comes from standard input
    for line in sys.stdin:
        doc_id, term, idf, freq, norm_fact = line.strip().split("\t")
        doc_id = int(doc_id)
        print(f"{doc_id%3}\t{term}\t{idf}\t{doc_id}\t{freq}\t{norm_fact}")


if __name__ == "__main__":
    main()
