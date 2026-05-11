from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_CHUNK_SIZE = 150
DEFAULT_CHUNK_OVERLAP = 20
DEFAULT_SEPARATORS = [" "]


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=DEFAULT_CHUNK_SIZE,
    chunk_overlap=DEFAULT_CHUNK_OVERLAP,
    separators=DEFAULT_SEPARATORS,
)


def chunk_content(content: str) -> list[str]:
    """Split incoming content into chunks for embedding/indexing."""
    return text_splitter.split_text(content.strip())
