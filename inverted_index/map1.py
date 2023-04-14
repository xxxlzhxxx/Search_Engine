#!/usr/bin/env python3
"""Map 1."""
import sys
import csv
import re

csv.field_size_limit(sys.maxsize)
with open("stopwords.txt") as f:
    stopwords = f.read().splitlines()

def clean_query(line) -> list:
    whole = line[1] + " " + line[2]
    whole = re.sub(r"[^a-zA-Z0-9 ]+", "", whole)
    whole = whole.casefold()
    tokens = whole.split()
    tokens_without_stopwords = [word for word in tokens if not word in stopwords]
    return int(line[0]), tokens_without_stopwords

def main():
    # Input comes from standard input
    lines = csv.reader(sys.stdin, delimiter=',')
    for line in lines:
        doc_id, tokens = clean_query(line)
        for token in tokens:
            print(f"{token}\t{doc_id}")


if __name__ == "__main__":
    main()
