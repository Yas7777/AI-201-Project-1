import os

# -------------------------------------------------------------------
# Base paths -  We could just use relative paths
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")

RAW_TEXT_PATH = os.path.join(DATA_PATH, "raw")
CLEANED_TEXT_PATH = os.path.join(DATA_PATH, "cleaned")
CHUNKS_PATH = os.path.join(DATA_PATH, "chunks.json")
CHROMA_PATH = os.path.join(DATA_PATH, "chroma_db")

# -------------------------------------------------------------------
# Chunking settings from planning.md
# -------------------------------------------------------------------
# The plan specifies paragraph-based chunks of approximately 600–800
# characters with 150 characters of overlap.
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Long-form article chunks should carry enough semantic context.
MIN_ARTICLE_CHUNK_LENGTH = 100

# A Playbill listing can be short but still useful, for example:
# "Show: Wicked | Theatre: Gershwin Theatre"
MIN_LISTING_CHUNK_LENGTH = 20

# -------------------------------------------------------------------
# Embedding and retrieval settings
# -------------------------------------------------------------------
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "broadway_documents"
TOP_K = 5

# -------------------------------------------------------------------
# Web request settings
# -------------------------------------------------------------------
REQUEST_TIMEOUT_SECONDS = 25
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)

# -------------------------------------------------------------------
# Broadway website sources
# -------------------------------------------------------------------
# kind="playbill_listing": keep each Playbill show card as its own chunk.
# kind="article": extract the long-form webpage body and split it into
# paragraph-aware chunks.
SOURCES = [
    {
        "document_name": "Playbill — Broadway Shows",
        "url": "https://playbill.com/shows/broadway",
        "kind": "playbill_listing",
    },
    {
        "document_name": "Playbill — Off-Broadway Shows",
        "url": "https://playbill.com/shows/offbroadway",
        "kind": "playbill_listing",
    },
    {
        "document_name": "Playbill — Schedule of Upcoming and Announced Broadway Shows",
        "url": "https://playbill.com/article/schedule-of-upcoming-and-announced-broadway-shows",
        "kind": "article",
    },
    {
        "document_name": "New York Theatre Guide — Best Broadway Plays in New York",
        "url": "https://www.newyorktheatreguide.com/theatre-news/news/top-broadway-plays",
        "kind": "article",
    },
    {
        "document_name": "New York Theatre Guide — Best-Reviewed Broadway Shows in New York",
        "url": "https://www.newyorktheatreguide.com/theatre-news/news/best-reviewed-broadway-shows-in-new-york",
        "kind": "article",
    },
    {
        "document_name": "TodayTix - NYT Critics picks",
        "url": "https://www.todaytix.com/nyc/collections/nyt-critics-picks",
        "kind": "article",
    },
    {
        "document_name": "Deadline — Broadway’s Spring 2026 Season: All of Deadline’s Reviews",
        "url": "https://deadline.com/2026/04/broadway-spring-2026-reviews-1236859028/",
        "kind": "article",
    },
    {
        "document_name": "Matthew Huff — All 30 of This Season’s New Broadway Shows, Ranked",
        "url": "https://huffmatt.substack.com/p/2026-broadway-shows-ranked-tony-awards",
        "kind": "article",
    },
    {
        "document_name": "Travel + Leisure — I’ve Seen 36 Broadway Shows in the Last Year—Here Are My Top Summer Picks",
        "url": "https://www.travelandleisure.com/best-broadway-shows-to-see-this-summer-11955436",
        "kind": "article",
    },
    {
        "document_name": "Broadway.com — The Best Shows Coming to Broadway in 2026",
        "url": "https://www.broadway.com/broadway-guide/51/broadway-best-shows-2026/",
        "kind": "article",
    },
]
