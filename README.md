# Search_Engine

## MapReduce Pipeline

---

Stage 0 - Count Total Number of Documents:

Map:
- Input: Preprocessed documents with doc_id, cleaned and tokenized text.
- Emit (1) for each document.
- Output: (1) 

Reduce:
- Input: (1) pairs grouped by 1.
- Output: Total number of documents (N).

---

Stage 1 - Term-document pairs and IDF calculation:

Map:

- Input: Preprocessed documents with doc_id, cleaned and tokenized text.
- For each term in the document, emit a key-value pair (term, doc_id).
- Output: (term, doc_id) pairs for each term in every document.

Reduce:

- Input: (term, doc_id) pairs grouped by term.
- Create a list of unique doc_ids for each term.
- Calculate the inverse document frequency (IDF) for each term using the formula: IDF = log(N / df), where N is the total number of documents and df is the number of documents containing the term.
Output: (term, IDF, list_of_doc_ids) tuples.

---

Stage 2 - Term frequency and document normalization factor calculation:

Map:

- Input: (term, IDF, list_of_doc_ids) tuples from stage 1.
- Emit a key-value pair (doc_id, (term, IDF)) for each doc_id in the list_of_doc_ids.
- Output: (doc_id, (term, IDF)) pairs.

Reduce:

- Input: (doc_id, (term, IDF)) pairs grouped by doc_id.
- Calculate the term frequency (TF) for each term in the document.
- Calculate the document normalization factor.
- Output: (doc_id, term, IDF, TF, normalization_factor) tuples.

---

Stage 3 - Inverted index construction and segmentation:

Map:

- Input: (doc_id, term, IDF, TF, normalization_factor) tuples from stage 2.
- Emit a key-value pair ((doc_id % 3), (term, IDF, doc_id, TF, normalization_factor)).
- Output: ((doc_id % 3), (term, IDF, doc_id, TF, normalization_factor)) pairs.

Reduce:

- Input: ((doc_id % 3), (term, IDF, doc_id, TF, normalization_factor)) pairs grouped by (doc_id % 3) and sorted by term.
- Concatenate doc_id, TF, and normalization_factor for each term.
Emit the final inverted index entries in the format (term, IDF, doc_id_1, TF_1, normalization_factor_1, doc_id_2, TF_2, normalization_factor_2, ...).
- Output: Segmented inverted index files with terms and corresponding IDF, doc_id, TF, and normalization factor.
By following these three stages, the MapReduce pipeline processes the input documents and generates an efficient and segmented inverted index.