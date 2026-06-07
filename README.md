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

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
