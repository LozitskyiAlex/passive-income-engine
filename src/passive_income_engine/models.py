from dataclasses import dataclass, field
from typing import Any


@dataclass
class Item:
    id: str
    title: str
    url: str
    source: str
    description: str = ""
    category: str = ""
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
