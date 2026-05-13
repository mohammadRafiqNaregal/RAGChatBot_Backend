from services.document_indexing_service import _FAISS_FOLDER
from services.faiss_store import SimpleFaissStore
from models.access_control import ROLE_ADMIN, normalize_optional_department


def _load_store() -> SimpleFaissStore | None:
    try:
        return SimpleFaissStore.load(_FAISS_FOLDER)
    except FileNotFoundError:
        return None


def retrieve_relevant_chunks(
    query: str,
    current_user: dict,
    top_k: int = 5,
    department: str | None = None,
) -> list[dict]:
    store = _load_store()
    if store is None:
        return []

    department = normalize_optional_department(department)
    role = current_user.get("role")
    raw_results = store.search(query, top_k=max(top_k * 5, top_k))

    filtered_results: list[dict] = []
    for item in raw_results:
        metadata = item.get("metadata", {})

        if department and metadata.get("department") != department:
            continue

        allowed_roles = metadata.get("allowed_roles") or []
        if role != ROLE_ADMIN and role not in allowed_roles:
            continue

        filtered_results.append(item)
        if len(filtered_results) >= top_k:
            break

    return filtered_results