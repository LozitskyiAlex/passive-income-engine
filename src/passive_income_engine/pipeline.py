from collections.abc import Iterable
from .models import Item


class SourceAdapter:
    """Interface for a public data source."""

    name = "source"

    def collect(self) -> Iterable[dict]:
        raise NotImplementedError


def normalize(records: Iterable[dict], source: str) -> list[Item]:
    items: list[Item] = []
    seen: set[str] = set()

    for record in records:
        item_id = str(record.get("id") or record.get("url") or "").strip()
        title = str(record.get("title") or "").strip()
        url = str(record.get("url") or "").strip()

        if not item_id or not title or not url or item_id in seen:
            continue

        seen.add(item_id)
        items.append(
            Item(
                id=item_id,
                title=title,
                url=url,
                source=source,
                description=str(record.get("description") or "").strip(),
                category=str(record.get("category") or "").strip(),
                tags=[str(x).strip() for x in record.get("tags", []) if str(x).strip()],
                metadata=dict(record.get("metadata") or {}),
            )
        )

    return items
