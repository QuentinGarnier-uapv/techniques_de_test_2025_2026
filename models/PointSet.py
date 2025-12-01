from dataclasses import dataclass, field
from typing import List
from .Point import Point

@dataclass
class PointSet:
    points: List[Point] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        """Format: 4 bytes unsigned int count + each point (8 bytes)."""
        # TODO: Implémenter
        return b""

    @classmethod
    def from_bytes(cls, data: bytes) -> "PointSet":
        """Parse PointSet from bytes."""
        # TODO: Implémenter
        raise NotImplementedError("Non implémenté")