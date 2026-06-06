from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

# Requests and BeautifulSoup are required for downloading and parsing HTML.
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

# Trafilatura improves article extraction
import trafilatura

# config file to store constants and settings
from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CHUNKS_PATH,
    CLEANED_TEXT_PATH,
    MIN_ARTICLE_CHUNK_LENGTH,
    MIN_LISTING_CHUNK_LENGTH,
    RAW_TEXT_PATH,
    REQUEST_TIMEOUT_SECONDS,
    SOURCES,
    USER_AGENT,
)
BOILERPLATE_PATTERNS = [
    r"^home$",
    r"^menu$",
    r"^site navigation$",
    r"^skip to (main )?content$",
    r"^shows?$",
    r"^news$",
    r"^reviews?$",
    r"^tickets?$",
    r"^get tickets?$",
    r"^buy tickets?$",
    r"^view details$",
    r"^read more\.?$",
    r"^read the full review\.?$",
    r"^subscribe.*$",
    r"^sign up.*$",
    r"^privacy policy$",
    r"^cookie policy$",
    r"^terms.*$",
    r"^contact us$",
    r"^advertise.*$",
    r"^careers.*$",
    r"^facebook$",
    r"^instagram$",
    r"^tiktok$",
    r"^threads$",
    r"^youtube$",
    r"^x$",
    r"^advertisement$",
    r"^related articles?$",
    r"^related stories$",
    r"^latest news$",
    r"^follow us$",
    r"^newsletter.*$",
    r"^copyright.*$",
    r"^©.*$",
]

BOILERPLATE_REGEXES = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in BOILERPLATE_PATTERNS
]

IGNORED_LISTING_HEADINGS = {
    "site navigation",
    "what’s playing on broadway and beyond",
    "what's playing on broadway and beyond",
    "now on broadway",
    "off-broadway",
    "broadway shows",
    "playbill editorial",
    "industry resources",
    "more from playbill",
    "sort by",
}

#-------------------------------------------------------------------
# CLEANING AND EXTRACTION
# -------------------------------------------------------------------
def ensure_output_folders() -> None:
    """Create folders for downloaded HTML, cleaned text, and chunks."""
    Path(RAW_TEXT_PATH).mkdir(parents=True, exist_ok=True)
    Path(CLEANED_TEXT_PATH).mkdir(parents=True, exist_ok=True)
    Path(CHUNKS_PATH).parent.mkdir(parents=True, exist_ok=True)


def safe_filename(name: str) -> str:
    """Create a readable filename without punctuation that breaks paths."""
    cleaned = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", "_", cleaned).strip("_")
    return cleaned[:140] or "document"


def normalize_text(text: str) -> str:
    """Decode entities and collapse unnecessary whitespace."""
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = text.replace("\ufeff", "")
    text = text.replace("\u200b", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_boilerplate_line(line: str) -> bool:
    """Identify obvious standalone navigation and footer lines."""
    line = normalize_text(line)

    if not line:
        return True

    if re.fullmatch(r"[-–—|•·\s]+", line):
        return True

    return any(regex.match(line) for regex in BOILERPLATE_REGEXES)


def remove_boilerplate_lines(text: str) -> str:
    """Remove obvious standalone clutter while preserving content."""
    kept_lines = []

    for raw_line in text.splitlines():
        line = normalize_text(raw_line)

        if not is_boilerplate_line(line):
            kept_lines.append(line)

    return normalize_text("\n".join(kept_lines))


def fetch_html(url: str) -> str:
    """Download one webpage."""
    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    response.raise_for_status()

    if not response.text.strip():
        raise ValueError(f"Downloaded an empty page: {url}")

    return response.text


def remove_non_content_tags(soup: BeautifulSoup) -> None:
    """Remove tags that should never become retrieval context."""
    for tag in soup.select(
        "script, style, noscript, svg, canvas, iframe, "
        "nav, header, footer, aside, form, button"
    ):
        tag.decompose()


# -------------------------------------------------------------------
# Article extraction
# -------------------------------------------------------------------
def extract_article_text(raw_html: str) -> str:
    """Extract readable long-form article text."""
    if trafilatura is not None:
        extracted = trafilatura.extract(
            raw_html,
            include_comments=False,
            include_tables=False,
            include_links=False,
            output_format="txt",
            favor_precision=True,
        )

        if extracted and len(extracted.strip()) >= MIN_ARTICLE_CHUNK_LENGTH:
            return remove_boilerplate_lines(extracted)

    soup = BeautifulSoup(raw_html, "html.parser")
    remove_non_content_tags(soup)

    container = soup.find("article") or soup.find("main") or soup.body or soup
    return remove_boilerplate_lines(container.get_text("\n", strip=True))


# -------------------------------------------------------------------
# Playbill listing extraction
# -------------------------------------------------------------------
def find_listing_container(heading: Tag) -> Tag:
    """Find a compact Playbill card containing the heading and its details."""
    best_container = heading
    current: Tag = heading

    for _ in range(6):
        parent = current.parent

        if not isinstance(parent, Tag):
            break

        text = normalize_text(parent.get_text(" | ", strip=True))

        if len(text) > 700:
            break

        best_container = parent
        current = parent

    return best_container


def clean_listing_details(details: str) -> str:
    """Remove controls from a Playbill show card."""
    details = re.sub(
        r"\b(View Details|Buy Tickets|Trending)\b",
        " ",
        details,
        flags=re.IGNORECASE,
    )
    details = re.sub(r"\s*\|\s*", "\n", details)
    details = re.sub(r"\n{2,}", "\n", details)
    return normalize_text(details)


def extract_playbill_listing_records(raw_html: str) -> list[str]:
    """Extract one focused record per Playbill show card."""
    soup = BeautifulSoup(raw_html, "html.parser")
    remove_non_content_tags(soup)

    records: list[str] = []
    seen_titles: set[str] = set()

    for heading in soup.find_all(["h3", "h4"]):
        title = normalize_text(heading.get_text(" ", strip=True))

        if not title or title.lower() in IGNORED_LISTING_HEADINGS:
            continue

        if len(title) > 140:
            continue

        title_key = title.casefold()

        if title_key in seen_titles:
            continue

        container = find_listing_container(heading)
        details = clean_listing_details(container.get_text(" | ", strip=True))

        # A useful record must contain something besides the heading itself.
        if not details or details.casefold() == title_key:
            continue

        record = normalize_text(
            f"Show: {title}\n"
            f"Details:\n{details}"
        )

        if len(record) < MIN_LISTING_CHUNK_LENGTH:
            continue

        seen_titles.add(title_key)
        records.append(record)

    return records


# -------------------------------------------------------------------
# Download and clean the configured webpages
# -------------------------------------------------------------------
def load_documents() -> list[dict[str, Any]]:
    """Download every configured URL and save its readable text."""
    ensure_output_folders()
    documents: list[dict[str, Any]] = []

    for source in SOURCES:
        document_name = source["document_name"]
        url = source["url"]
        kind = source["kind"]
        filename = safe_filename(document_name)

        print(f"\nDownloading: {document_name}")
        print(f"URL: {url}")

        try:
            raw_html = fetch_html(url)
        except Exception as error:
            print(f"WARNING: Could not download this source: {error}")
            print("Skipping it and continuing with the remaining sources.")
            continue

        raw_path = Path(RAW_TEXT_PATH) / f"{filename}.html"
        raw_path.write_text(raw_html, encoding="utf-8")

        if kind == "playbill_listing":
            records = extract_playbill_listing_records(raw_html)

            if not records:
                print("WARNING: No Playbill show cards were extracted.")
                print("The website HTML may have changed. Skipping this source.")
                continue

            cleaned_text = "\n\n".join(records)
        else:
            records = []
            cleaned_text = extract_article_text(raw_html)

        if len(cleaned_text.strip()) < MIN_ARTICLE_CHUNK_LENGTH:
            print("WARNING: Extracted text was too short. Skipping this source.")
            continue

        cleaned_path = Path(CLEANED_TEXT_PATH) / f"{filename}.txt"
        cleaned_path.write_text(cleaned_text, encoding="utf-8")

        documents.append(
            {
                "document_name": document_name,
                "source_url": url,
                "kind": kind,
                "text": cleaned_text,
                "records": records,
            }
        )

        if records:
            print(f"Extracted {len(records)} Playbill show record(s).")
        else:
            print(f"Extracted {len(cleaned_text)} cleaned character(s).")

    print(f"\nLoaded {len(documents)} of {len(SOURCES)} source(s).")
    return documents


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Chunking
# Article chunks target a maximum of 800 characters, with up to
# 150 characters of overlap between adjacent chunks.
# Playbill listing records are kept as individual focused chunks.
# -------------------------------------------------------------------# -------------------------------------------------------------------
def find_natural_split_position(text: str, maximum_length: int) -> int:
    """Choose a sentence or word boundary near the chunk-size limit."""
    if len(text) <= maximum_length:
        return len(text)

    window = text[:maximum_length]
    search_start = int(maximum_length * 0.55)
    tail = window[search_start:]
    sentence_matches = list(re.finditer(r"[.!?][\"')\]]?\s+", tail))

    if sentence_matches:
        return search_start + sentence_matches[-1].end()

    space_index = window.rfind(" ", search_start)
    return space_index if space_index != -1 else maximum_length


def get_overlap_text(text: str, overlap_size: int) -> str:
    """Return a readable overlap for the next article chunk."""
    if len(text) <= overlap_size:
        return text.strip()

    overlap_text = text[-overlap_size:]
    first_space = overlap_text.find(" ")

    if first_space != -1:
        overlap_text = overlap_text[first_space + 1:]

    return overlap_text.strip()


def split_long_text(text: str) -> list[str]:
    """Split long article text into readable overlapping pieces."""
    pieces = []
    remaining = text.strip()

    while len(remaining) > CHUNK_SIZE:
        split_at = find_natural_split_position(remaining, CHUNK_SIZE)
        piece = remaining[:split_at].strip()

        if len(piece) >= MIN_ARTICLE_CHUNK_LENGTH:
            pieces.append(piece)

        overlap = get_overlap_text(piece, CHUNK_OVERLAP)
        remaining = remaining[split_at:].strip()

        if overlap:
            remaining = f"{overlap} {remaining}".strip()

    if len(remaining) >= MIN_ARTICLE_CHUNK_LENGTH:
        pieces.append(remaining)

    return pieces


def make_chunk(
    *,
    chunk_id: str,
    document_name: str,
    source_url: str,
    text: str,
    chunk_position: int,
) -> dict[str, Any]:
    """Build one metadata-rich chunk."""
    return {
        "chunk_id": chunk_id,
        "document_name": document_name,
        "source_url": source_url,
        "chunk_position": chunk_position,
        "text": text.strip(),
    }


def chunk_listing_document(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Keep each Playbill listing as its own focused chunk."""
    chunks = []
    prefix = safe_filename(document["document_name"]).lower()

    for position, record in enumerate(document["records"]):
        if len(record) < MIN_LISTING_CHUNK_LENGTH:
            continue

        chunks.append(
            make_chunk(
                chunk_id=f"{prefix}_{position}",
                document_name=document["document_name"],
                source_url=document["source_url"],
                text=record,
                chunk_position=position,
            )
        )

    return chunks


def chunk_article_document(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Create paragraph-aware chunks for a long-form article."""
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n{2,}", document["text"])
        if paragraph.strip()
    ]

    chunks = []
    current = ""
    prefix = safe_filename(document["document_name"]).lower()

    def save_chunk(text: str) -> None:
        text = text.strip()

        if len(text) < MIN_ARTICLE_CHUNK_LENGTH:
            return

        position = len(chunks)
        chunks.append(
            make_chunk(
                chunk_id=f"{prefix}_{position}",
                document_name=document["document_name"],
                source_url=document["source_url"],
                text=text,
                chunk_position=position,
            )
        )

    for paragraph in paragraphs:
        if len(paragraph) > CHUNK_SIZE:
            if current:
                save_chunk(current)
                current = ""

            for piece in split_long_text(paragraph):
                save_chunk(piece)

            continue

        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph

        if len(candidate) <= CHUNK_SIZE:
            current = candidate
            continue

        save_chunk(current)
        overlap = get_overlap_text(current, CHUNK_OVERLAP)
        current = f"{overlap}\n\n{paragraph}".strip() if overlap else paragraph

    if current:
        save_chunk(current)

    return chunks


def chunk_all_documents(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Chunk every document according to its source type."""
    all_chunks = []

    for document in documents:
        if document["kind"] == "playbill_listing":
            chunks = chunk_listing_document(document)
        else:
            chunks = chunk_article_document(document)

        all_chunks.extend(chunks)
        print(f"Created {len(chunks)} chunk(s) from {document['document_name']}")

    return all_chunks


def validate_chunks(chunks: list[dict[str, Any]]) -> None:
    """Fail early if a chunk is missing metadata needed by generator.py."""
    required_fields = {
        "chunk_id",
        "document_name",
        "source_url",
        "chunk_position",
        "text",
    }
    seen_chunk_ids: set[str] = set()

    for index, chunk in enumerate(chunks):
        missing = required_fields - set(chunk)
        if missing:
            raise ValueError(
                f"Chunk {index} is missing required field(s): {sorted(missing)}"
            )

        if not str(chunk["text"]).strip():
            raise ValueError(f"Chunk {index} has empty text.")

        chunk_id = str(chunk["chunk_id"])
        if chunk_id in seen_chunk_ids:
            raise ValueError(f"Duplicate chunk_id detected: {chunk_id}")

        seen_chunk_ids.add(chunk_id)


def save_chunks(chunks: list[dict[str, Any]]) -> None:
    """Validate and write chunks to JSON for generator.py."""
    validate_chunks(chunks)

    with open(CHUNKS_PATH, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(chunks)} total chunk(s) to {CHUNKS_PATH}")


def print_sample_cleaned_document(documents: list[dict[str, Any]]) -> None:
    """Print a sample for a manual cleaning check."""
    if not documents:
        return

    sample = documents[0]
    print("\n" + "=" * 80)
    print("MANUAL CLEANING CHECK")
    print("=" * 80)
    print(f"Document: {sample['document_name']}")
    print(f"URL: {sample['source_url']}\n")
    print(sample["text"][:4000])
    print("\n" + "=" * 80)

## MAIN FUNCTION ##
def main() -> None:
    """Run website ingestion, cleaning, chunking, and JSON export."""
    documents = load_documents()

    if not documents:
        raise RuntimeError(
            "No webpages could be ingested. Review the warnings above."
        )

    print_sample_cleaned_document(documents)
    chunks = chunk_all_documents(documents)

    if not chunks:
        raise RuntimeError("No chunks were created.")

    save_chunks(chunks)


if __name__ == "__main__":
    main()

