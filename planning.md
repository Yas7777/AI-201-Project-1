# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I chose Broadway as my domain. It is not easy to find the best shows to watch in NYC, as there are a lot and a lot of them are very limited runs. As a local its important to prioritse time for the limited runs, while making sure that long standing shows dont have cast changes etc along with checking reviews. It is a lot of back and forth with multiple substacks and google searches to make this choice on which show to watch.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| Source | Description | URL or location |
|---|---|---|
| Playbill — Broadway Shows | A current directory of Broadway productions, including show titles, theatres, and closing dates. Useful for answering questions about what is currently playing on Broadway. | `https://playbill.com/shows/broadway` |
| Playbill — Off-Broadway Shows | A directory of current and upcoming Off-Broadway productions, including theatres, preview dates, and closing dates. Useful for recommending shows outside the main Broadway theatre district. | `https://playbill.com/shows/offbroadway` |
| Playbill — Schedule of Upcoming and Announced Broadway Shows | A regularly updated guide to upcoming Broadway productions, including previews, opening dates, theatres, cast members, and short plot summaries. | `https://playbill.com/article/schedule-of-upcoming-and-announced-broadway-shows` |
| New York Theatre Guide — Best Broadway Plays in New York | A curated guide to notable Broadway plays currently running, with descriptions, genres, notable cast members, and reasons to see each show. | `https://www.newyorktheatreguide.com/theatre-news/news/top-broadway-plays` |
| New York Theatre Guide — Best-Reviewed Broadway Shows in New York | A curated list of critically acclaimed Broadway and Off-Broadway shows, including review excerpts and descriptions of each production. | `https://www.newyorktheatreguide.com/theatre-news/news/best-reviewed-broadway-shows-in-new-york` |
| The New York Times — 9 Shows Our Theater Critics Are Talking About | A critic-curated guide to notable productions, including review summaries and recommendations for Broadway and Off-Broadway shows. | `https://www.nytimes.com/2026/04/17/theater/salesman-giant-cats-becky-shaw-proof-broadway.html` |
| Deadline — Broadway’s Spring 2026 Season: All of Deadline’s Reviews | A collection of Deadline’s reviews for Spring 2026 Broadway productions, including opening dates, venues, casts, running times, and critical takeaways. | `https://deadline.com/2026/04/broadway-spring-2026-reviews-1236859028/` |
| Matthew Huff — All 30 of This Season’s New Broadway Shows, Ranked | A ranked list of the 2025–2026 season’s Tony Award-eligible Broadway shows based on the author’s firsthand viewing experience. Useful for comparison and recommendation questions. | `https://huffmatt.substack.com/p/2026-broadway-shows-ranked-tony-awards` |
| Travel + Leisure — I’ve Seen 36 Broadway Shows in the Last Year: Here Are My Top Summer Picks | A recommendation article highlighting ten Broadway shows for summer visitors, with descriptions and explanations of why each show stands out. | `https://www.travelandleisure.com/best-broadway-shows-to-see-this-summer-11955436` |
| Broadway.com — The Best Shows Coming to Broadway in 2026 | A guide to anticipated Broadway productions arriving in 2026, including descriptions and expected opening information. | `https://www.broadway.com/buzz/206109/the-best-shows-coming-to-broadway-in-2026/` |
  
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 600–800

I will try and use paragraph-based chunking with approximately 600–800 characters

Using less than 600 may be too small for review text. There is alot of context required in this domain and to make connections between opinions (reviews) and facts (date, show title etc). With a smaller chunk size, these details may be split.


**Overlap:** 150

150 feels like a good size for oerlap. This should should preserve complete opinions while keeping retrieved chunks focused enough for recommendations and comparisons.

**Reasoning:**


---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
