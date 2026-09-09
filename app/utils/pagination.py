from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    items: Sequence[T]
    total: int
    skip: int
    limit: int

    @property
    def has_next(self) -> bool:
        return self.skip + self.limit < self.total

    @property
    def has_previous(self) -> bool:
        return self.skip > 0


def paginate(items: Sequence[T], total: int, skip: int, limit: int) -> dict:
    return {
        "items": list(items),
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_previous": skip > 0,
    }
