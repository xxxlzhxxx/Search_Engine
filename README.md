# Search_Engine

## MapReduce Pipeline


Stage 0 - Count Total Number of Documents:

---

Stage 1 - Term-document pairs and TF/IDF calculation:

Map:

- Input: Preprocessed documents with doc_id, cleaned and tokenized text.
- For each term in the document, emit a key-value pair (term, doc_id).
- Output: (term, doc_id) pairs for each term in every document.

Reduce:

- Input: (term, doc_id) pairs grouped by term.
- Create a list of unique doc_ids for each term.
- Calculate the document frequency (df) for each term.
- Calculate the inverse document frequency (IDF) for each term using the formula: IDF = log(N / df), where N is the total number of documents and df is the number of documents containing the term.
Output: (term, IDF, list[doc_id], list[TF]) tuples.

---

Stage 2 - Document normalization factor calculation:

Map:

- Input: (term, IDF, list[doc_id] list[TF]) tuples.
- Emit a key-value pair (doc_id, (term, IDF, TF)) for each doc_id in the list_of_doc_ids.
- Output: (doc_id, (term, IDF, TF)) pairs.

Reduce:

- Input: (doc_id, (term, IDF)) pairs grouped by doc_id.
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