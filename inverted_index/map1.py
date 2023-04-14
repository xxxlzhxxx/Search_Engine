#!/usr/bin/env python3
"""Map 1."""
import sys
from utils import clean_query

def main():
    # Input comes from standard input
    for query in sys.stdin:
        doc_id, tokens = clean_query(query)
        for token in tokens:
            print(f"{token}\t{doc_id}")


if __name__ == "__main__":
    main()
