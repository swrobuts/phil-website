# Semantic Search (RAG)

Phil uses Retrieval-Augmented Generation to find relevant past emails
even when keyword search would fail.

## The problem RAG solves

A keyword search for "budget" misses an email titled "Cost allocation for Q3."
RAG finds it because the vector embeddings are semantically similar.

## How it works

1. When a mail is triaged, its text (subject + body + attachment summaries) is embedded
   using `text-embedding-3-small` (OpenAI) or equivalent
2. The embedding is stored in ChromaDB at `/tmp/phil_chroma`
3. At query time, the user's question is embedded and the top-3 nearest neighbours
   are retrieved
4. These are injected into the chat context as `MAILHISTORIE` blocks

## Vector store location

ChromaDB stores its files at `/tmp/phil_chroma` to avoid OneDrive sync conflicts
(memory-mapped HNSW files must not live on network drives).

## Ontology layer

In addition to vector search, Phil maintains an RDF ontology store (`OntologyStore`)
that maps extracted entities (persons, projects, deadlines) as structured triples.
This allows precise graph queries alongside fuzzy semantic search.

!!! note "DE"
    Phil kann deine E-Mails semantisch durchsuchen — nicht nur nach Stichwörtern,
    sondern nach Bedeutung. Ähnliche Mails aus der Vergangenheit werden automatisch
    als Kontext eingeblendet.
