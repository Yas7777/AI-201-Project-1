# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

I chose Broadway as my domain. It is not easy to find the best shows to watch in NYC, as there are a lot of shows and a lot of them are very limited runs. As a local its important to prioritse time for the limited runs, while making sure that long standing shows dont have cast changes etc along with checking reviews. It is a lot of back and forth with multiple substacks and google searches to make this choice on which show to watch.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #  | Source                                                                                        | Description                                                                                                                                                                                   | URL or location                                                                                  |
| -- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 1  | Playbill — Broadway Shows                                                                     | A current directory of Broadway productions, including show titles, theatres, and closing dates. Useful for answering questions about what is currently playing on Broadway.                  | `https://playbill.com/shows/broadway`                                                            |
| 2  | Playbill — Off-Broadway Shows                                                                 | A directory of current and upcoming Off-Broadway productions, including theatres, preview dates, and closing dates. Useful for recommending shows outside the main Broadway theatre district. | `https://playbill.com/shows/offbroadway`                                                         |
| 3  | Playbill — Schedule of Upcoming and Announced Broadway Shows                                  | A regularly updated guide to upcoming Broadway productions, including previews, opening dates, theatres, cast members, and short plot summaries.                                              | `https://playbill.com/article/schedule-of-upcoming-and-announced-broadway-shows`                 |
| 4  | New York Theatre Guide — Best Broadway Plays in New York                                      | A curated guide to notable Broadway plays currently running, with descriptions, genres, notable cast members, and reasons to see each show.                                                   | `https://www.newyorktheatreguide.com/theatre-news/news/top-broadway-plays`                       |
| 5  | New York Theatre Guide — Best-Reviewed Broadway Shows in New York                             | A curated list of critically acclaimed Broadway and Off-Broadway shows, including review excerpts and descriptions of each production.                                                        | `https://www.newyorktheatreguide.com/theatre-news/news/best-reviewed-broadway-shows-in-new-york` |
| 6  | TodayTix — NYT Critics Picks                                                                  | A critic-curated guide to notable productions, including review summaries and recommendations for Broadway and Off-Broadway shows.                                                            | `https://www.todaytix.com/nyc/collections/nyt-critics-picks/`                                    |
| 7  | Deadline — Broadway’s Spring 2026 Season: All of Deadline’s Reviews                           | A collection of Deadline’s reviews for Spring 2026 Broadway productions, including opening dates, venues, casts, running times, and critical takeaways.                                       | `https://deadline.com/2026/04/broadway-spring-2026-reviews-1236859028/`                          |
| 8  | Matthew Huff — All 30 of This Season’s New Broadway Shows, Ranked                             | A ranked list of the 2025–2026 season’s Tony Award-eligible Broadway shows based on the author’s firsthand viewing experience. Useful for comparison and recommendation questions.            | `https://huffmatt.substack.com/p/2026-broadway-shows-ranked-tony-awards`                         |
| 9  | Travel + Leisure — I’ve Seen 36 Broadway Shows in the Last Year: Here Are My Top Summer Picks | A recommendation article highlighting ten Broadway shows for summer visitors, with descriptions and explanations of why each show stands out.                                                 | `https://www.travelandleisure.com/best-broadway-shows-to-see-this-summer-11955436`               |
| 10 | Broadway.com — The Best Shows Coming to Broadway in 2026                                      | A guide to anticipated Broadway productions arriving in 2026, including descriptions and expected opening information.                                                                        | `https://www.broadway.com/buzz/206109/the-best-shows-coming-to-broadway-in-2026/`                |

  
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 600–800
I will use recursive-based chunking with approximately 600–800 characters
Using less than 600 may be too small for review text. There is alot of context required in this domain and to make connections between opinions (reviews) and facts (date, show title etc). With a smaller chunk size, these details may be split.


**Overlap:** 150
150 feels like a good size for overlap. This should should preserve complete opinions while keeping retrieved chunks focused enough for recommendations and comparisons.

**Reasoning:**
These choices I have made were estimates based on the sources. Recursive-based chunking works well because it attempts to keep related text together before splitting at smaller boundaries when necessary. The 600–800 character range provides enough context for comparisons and recommendations while keeping each chunk focused enough for retrieval.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 

**Top-k:** 7
This is a reasonable start to the project. Less than 5 seems too low to produce useful info. Upon trial and error between 5 and 7 - 7 worked best for our usecase here. 

**Production tradeoff reflection:**
Given the small sample size / review dataset, all-MiniLM-L6-v2 is a practical choice because it can be run locally. For a production system with more documents, I would compare embedding models based on its ability to perform well with a large sample size, its retrieval accuracy etc. I would also test different top-k values and chunk sizes using sample questions to get the most accurate recommendations.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

## Part 1: Evaluation Questions and Expected Answers

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which Broadway show is a comedic reimagining of *Titanic* featuring Céline Dion songs? | *Titaníque*. It is a campy comedic reimagining of *Titanic* featuring the songs of Céline Dion. |
| 2 | When does *Giant* close, and who stars in it? | *Giant* closes on June 28, 2026. It stars John Lithgow as Roald Dahl. |
| 3 | Where is *Kenrex* currently playing? | *Kenrex* is currently playing at the Lucille Lortel Theatre. |
| 4 | What is *Every Brilliant Thing* about? | *Every Brilliant Thing* is a solo show about a person looking back on their life through a list of wonderful things, both big and small, that make life worth living. |
| 5 | What Broadway show would be a good choice for a family that enjoys Harry Potter? | *Harry Potter and the Cursed Child* would be a good choice because it continues the story of the Harry Potter universe on stage. |
| 6 | Which Broadway musical would be a good choice for someone who wants to see a long-running classic? | *Chicago* would be a good choice because it is a long-running Broadway classic. |
| 7 | What is *Operation Mincemeat* about? | *Operation Mincemeat* is a comedic musical based on the true story of a British intelligence operation during World War II. The plan involved using a corpse carrying fake documents to mislead Nazi Germany about the Allies' invasion plans. |
| 8 | What is notable about *Maybe Happy Ending* according to the retrieved reviews? | The reviews praise *Maybe Happy Ending* for being charming, heartfelt, visually impressive, and emotionally moving. It tells an unusual love story about two robots and explores connection, companionship, and loneliness. |
| 9 | How much does a front-row ticket for *Hamilton* cost this Friday? | No information. |
| 10 | What is the best pizza place in Manhattan? | No information  |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. I think my sources are not varied enough. I did not want to include r/broadway and similair subreddits as I am unclear on how to process that.

2. The cleanup is the most important aspect of theis project. The playbill links are especially noisy as they are ad-heavy and have a lot of purchase links etc. Given that, I believe the chunks will be hard to fully clean as  they may split key information across various important context.

---

## Architecture

```text
┌──────────────────────────────┐
│ 1. DOCUMENT INGESTION        │
│                              │
│ Website URLS                 │
│ Load Broadway articles       │
│ and reviews                  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ 2. CHUNKING                  │
│ Paragraph-based chunks       │
│ Target max: 800 characters   │
│ Overlap: 150 characters      │
│                              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ 3. EMBEDDING + VECTOR STORE  │
│                              │
│ sentence-transformers        │
│ all-MiniLM-L6-v2             │
│ Store embeddings in ChromaDB │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ 4. RETRIEVAL                 │
│                              │
│ ChromaDB similarity search   │
│ Retrieve top-k = 5 chunks    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ 5. GENERATION                │
│                              │
│ OpenAI API                   │
│ Generate an answer using     │
│ retrieved context            │
└──────────────────────────────┘
```

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

- Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
I plan to use Github Copilot and ChatGPT

- What you'll give it as input (which sections of this planning.md, which requirements)
I plan to provide the Source, Architecture as a starting point

- What you expect it to produce
I am expecting it to produce a decent clean up strategy given that my links are fairly straightforward

- How you'll verify the output matches your spec
I plan to check the chunking.json file it will provide to see the quality of the chunks it will produce. I am aware that I will have to reiterate depedning on how the chubnk sizing and its results. 

**Milestone 4 — Embedding and retrieval:**
- Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
I plan to use Github Copilot, ChatGPT, ClaudeCode

- What you'll give it as input (which sections of this planning.md, which requirements)
I plan to provide the Source, Architecture as a starting point

- What you expect it to produce
I am expecting it to produce a retrieval boilerplate code relevant to my domain / broadway source (it was hard to clean up - so i expect some difficulty here). I also want it to write functions that accepts a question and returns the most relevant chunks with their source information and distance scores.

- How you'll verify the output matches your spec
I will run at least three evaluation questions and inspect the returned chunks and distance scores.

**Milestone 5 — Generation and interface:**

- Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
I plan to use Github Copilot, ChatGPT, ClaudeCode

- What you'll give it as input (which sections of this planning.md, which requirements)
I plan to provide the Source, Architecture as a starting point

- What you expect it to produce
I am expecting it to produce a generator and app.py boiler plate code. I expect some minor work to be done with the way the answers are generated (perhaps if its out of domain range) and I would like the app to look fun.

- How you'll verify the output matches your spec
I will test the appl with both in-scope and out-of-scope questions. I will confirm that relevant questions receive grounded answers with source attribution and unsupported questions receive a clear response explaining that there is not enough information, and the interface displays the answer and sources correctly.