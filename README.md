# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

I chose Broadway as my domain. It is not easy to find the best shows to watch in NYC, as there are a lot of shows and a lot of them are very limited runs. As a local its important to prioritse time for the limited runs, while making sure that long standing shows dont have cast changes etc along with checking reviews. It is a lot of back and forth with multiple substacks and google searches to make this choice on which show to watch.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #  | Source                                                                                        | Type    | URL or file path                                                                                 |
| -- | --------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------ |
| 1  | Playbill — Broadway Shows                                                                     | Website | `https://playbill.com/shows/broadway`                                                            |
| 2  | Playbill — Off-Broadway Shows                                                                 | Website | `https://playbill.com/shows/offbroadway`                                                         |
| 3  | Playbill — Schedule of Upcoming and Announced Broadway Shows                                  | Website | `https://playbill.com/article/schedule-of-upcoming-and-announced-broadway-shows`                 |
| 4  | New York Theatre Guide — Best Broadway Plays in New York                                      | Website | `https://www.newyorktheatreguide.com/theatre-news/news/top-broadway-plays`                       |
| 5  | New York Theatre Guide — Best-Reviewed Broadway Shows in New York                             | Website | `https://www.newyorktheatreguide.com/theatre-news/news/best-reviewed-broadway-shows-in-new-york` |
| 6  | TodayTix — NYT Critics Picks                                                                  | Website | `https://www.todaytix.com/nyc/collections/nyt-critics-picks/`                                    |
| 7  | Deadline — Broadway’s Spring 2026 Season: All of Deadline’s Reviews                           | Website | `https://deadline.com/2026/04/broadway-spring-2026-reviews-1236859028/`                          |
| 8  | Matthew Huff — All 30 of This Season’s New Broadway Shows, Ranked                             | Website | `https://huffmatt.substack.com/p/2026-broadway-shows-ranked-tony-awards`                         |
| 9  | Travel + Leisure — I’ve Seen 36 Broadway Shows in the Last Year: Here Are My Top Summer Picks | Website | `https://www.travelandleisure.com/best-broadway-shows-to-see-this-summer-11955436`               |
| 10 | Broadway.com — The Best Shows Coming to Broadway in 2026                                      | Website | `https://www.broadway.com/buzz/206109/the-best-shows-coming-to-broadway-in-2026/`                |


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 600-800
I will use recursive-based chunking with approximately 600–800 characters. Using less than 600 may be too small for review text. There is alot of context required in this domain and required to make connections between opinions (reviews) and facts (date, show title etc). With a smaller chunk size, these important details may be split.

**Overlap:** 150
150 feels like a good size for overlap. This should should preserve complete opinions while keeping retrieved chunks focused enough for recommendations and comparisons.

**Preprocessing you did before chunking**
Before chunking, I cleaned the webpage content to remove text such as navigation menus, cookie banners, headers, share buttons and other boilerplate text with regard to this project. I also removed unnecessary whitespace while preserving the content, such as show descriptions, theatre information, dates, reviews, rankings, and recommendations.

**Why these choices fit your documents:**
These choices I have made were estimates based on the sources. Recursive-based chunking works well because it attempts to keep related text together before splitting at smaller boundaries when necessary. The 600–800 character range provides enough context for comparisons and recommendations while keeping each chunk focused enough for retrieval.

**Final chunk count:** 224 chunks across 10 sources.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 

**Production tradeoff reflection:**
Given the small sample size / review dataset, all-MiniLM-L6-v2 is a practical choice because it can be run locally. For a production system with more documents, I would compare embedding models based on its ability to perform well with a large sample size, its retrieval accuracy etc. I would also test different top-k values and chunk sizes using sample questions to get the most accurate recommendations.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you fformatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The LLM is only supposed to answer from the retrieved Broadway documents. This is the prompt:

```text
You are a grounded Broadway RAG assistant.

You must answer using ONLY the provided retrieved document context.

Rules:
- Do not use outside knowledge.
- Do not guess.
- Do not make assumptions.
- If the context does not contain enough information to answer the question, say exactly:
  "I don't have enough information on that."
- Keep the answer concise and directly tied to the retrieved info.
```

**Structural Choices**
For each question, the retriever returns the top 7 relevant chunks from ChromaDB. Each chunk includes its document name, source URL, and text:
[Chunk 1]
Document: ...
Source URL: ...
Text: ...
This structure helps the model distinguish between separate retrieved excerpts and keeps the answer tied to the available evidence. The model temperature is set to 0 to reduce unnecessary variation and discourage unsupported answers.

It does not currently use a similarity-score threshold to remove low-relevance chunks. Instead, it retrieves the top 7 chunks for each query. If no chunks are returned, or if the retrieved context does not contain enough information, the system returns:

> "I don't have enough information on that."

**How source attribution is surfaced in the response:**
The system returns the generated answer together with a list of sources. Each source includes the document name and its original URL. Duplicate sources are removed so the same article is not displayed multiple times.

For clarity, the interface displays (up to) two sources from the highest-ranked retrieved chunks:

Document Name — Source URL

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

## Part 2: Evaluation Results

| #  | Question                                                                                           | Expected answer                                                                                                                                                                                                                        | System response (summarized)                                                                                                                                                               | Retrieval quality | Response accuracy |
| -- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- | ----------------- |
| 1  | Which Broadway show is a comedic reimagining of *Titanic* featuring Céline Dion songs?             | *Titaníque*. It is a comedic reimagining of *Titanic* featuring the songs of Céline Dion.                                                                                                                                              | *Titaníque* is a comedic reimagining of *Titanic* featuring the hits of Céline Dion.                                                                                                       | Relevant          | Accurate          |
| 2  | When does *Giant* close, and who stars in it?                                                      | *Giant* closes on June 28, 2026, and stars John Lithgow.                                                                                                                                                                               | *Giant* closes on June 28, 2026, and stars John Lithgow.                                                                                                                                   | Relevant          | Accurate          |
| 3  | Where is *Kenrex* currently playing?                                                               | *Kenrex* is currently playing at the Lucille Lortel Theatre.                                                                                                                                                                           | *Kenrex* is currently playing at the Lucille Lortel Theatre.                                                                                                                               | Relevant          | Accurate          |
| 4  | What is *Every Brilliant Thing* about?                                                             | *Every Brilliant Thing* is about a person who begins a list of things that make life worth living. The list becomes a lifelong project. The play includes audience interaction and explores depression and hope.                       | The system explained that the narrator creates a lifelong list of things that make life worth living. It also mentioned the audience interaction and the play's exploration of depression. | Relevant          | Accurate          |
| 5  | What Broadway show would be a good choice for a family that enjoys Harry Potter?                   | *Harry Potter and the Cursed Child* would be a good choice because it continues the story of the Harry Potter universe on stage.                                                                                                       | *Harry Potter and the Cursed Child* would be a good choice for a family that enjoys Harry Potter.                                                                                          | Relevant          | Accurate          |
| 6  | Which Broadway musical would be a good choice for someone who wants to see a long-running classic? | A suitable answer could include a long-running Broadway musical such as *The Lion King*, *Wicked*, *Hamilton*, or *Chicago*.                                                                                                           | The system recommended *The Lion King*, *Wicked*, and *Hamilton* as long-running classics.                                                                                                 | Relevant          | Accurate          |
| 7  | What is *Operation Mincemeat* about?                                                               | *Operation Mincemeat* is a comedic musical based on a real British intelligence operation during World War II. The operation involved using a corpse carrying fake documents to mislead Nazi Germany about the Allies' invasion plans. | The system responded that it did not have enough information to answer the question.                                                                                                       | Relevant       | Inaccurate        |
| 8  | What is notable about *Maybe Happy Ending* according to the retrieved reviews?                     | The reviews describe *Maybe Happy Ending* as a surprisingly human and emotionally moving romance between two robots. The show also won six awards at the 2025 Tony Awards.                                                             | The system explained that the show tells an unlikely but remarkably human love story between two fading robots. It also mentioned that it won six trophies at the 2025 Tony Awards.        | Relevant          | Accurate          |
| 9  | How much does a front-row ticket for *Hamilton* cost this Friday?                                  | The system should explain that it cannot answer the question from the retrieved documents because ticket prices are dynamic and date-specific. It should recommend checking an official ticketing website for the current price.       | The system responded that it did not have enough information to answer the question.                                                                                                       | Relevant          | Accurate          |
| 10 | What is the best pizza place in Manhattan?                                                         | The system should explain that the question is outside the scope of the Broadway and Off-Broadway knowledge base.                                                                                                                      | The system responded that it did not have enough information to answer the question.                                                                                                       | Off-target         | Accurate          |

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

## Failure Case Analysis

**Question that failed:**
What is Operation Mincemeat about?

**What the system returned:**
“I don't have enough information on that.”

**Root cause (tied to a specific pipeline stage):**
The failure occurred during the **retrieval stage**. Operation Mincemeat is a Broadway musical, so the question is within the domain scope of the system. However, the top retrieved chunks did not provide enough information about the show's plot for the model to generate an answer. The relevant description may have been removed during cleaning, or may not have ranked highly enough during similarity search. Because the generation prompt instructs the model to answer only from the retrieved context, the model did not invent an answer.

**What you would change to fix it:**
I would investigate the cleaned documents and generated chunks to confirm that a plot summary for Operation Mincemeat exists. If the information is not there, I would add or update a source document that includes a clear description of the show. If the information is present but was not retrieved, I would test larger top_k values, and review whether the relevant chunk appears. I would also check whether the show's title and plot summary were split across separate chunks. If so, I would adjust the chunking logic or overlap size so that the title and description remain together.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning.md file helped me define the scope of the project before writing the ingestion and retrieval code. It identified the sources, the type of questions the system should answer, and the chunking approach. This made it easier to decide what content to preserve during cleaning, such as show titles, theatres, etc. It also made me think of potential issues especially when it comes to cleaning up. 

**One way your implementation diverged from the spec, and why:**
My initial spec described a general recursive chunking approach with chunks of approximately 600–800 characters. During implementation, I adjusted the cleaning significantly along with the chunking logic to better preserve paragraphs and keep related details together, especially when a show title was followed by its theatre, plot summary, or review. This was extremely important because splitting those details across separate chunks could make the retrieval less accurate. I also refined the source list during implementation by replacing a paywalled source with a better source that could be ingested better. I also continously reiterated the clean up code, as I checked against the chunk.json to see it correctly cleaned up with each reiteration. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I provided my Broadway source list and the planning.md requirements in terms of ingesting the data.
- *What it produced:*
The AI generated an initial version of ingest.py that loaded the source documents, cleaned the extracted text, created chunks, and saved metadata for each chunk.
- *What I changed or overrode:*
I continously refined the chunking and cleaning logic to better preserve the relevant Broadway content and remove navigation text and other boilerplate content. In addition, I ensured that each chunk stored the required metadata fields, including the source name, source_url, and chunk_position. I also overrode the chunk size from 300 to 600.

**Instance 2**

- *What I gave the AI:*
I provided the retrieval requirements and the embedding model requirement (all-MiniLM-L6-v2)
- *What it produced:*
The AI generated and revised the retrieval logic in generator.py, including loading stored chunks, embedding them, querying ChromaDB, returning the top matching results, and using the retrieved context to generate an answer with source attribution
- *What I changed or overrode:*
I reviewed the returned chunks using test questions and adjusted the implementation so it answered only from the retrieved context rather than inventing details. I had also kept the retrieval value at a small top_k so the model received relevant context without being distracted by too many loosely related chunks. However, I increased it from 5 to 7 as I saw significant improvement in results. Better ingestion would have perhaps worked with the lower value of k. 