from dataclasses import dataclass, field
from typing import List
from .Point import Point
from .Triangle import Triangle

@dataclass
class Triangles:
    points: List[Point] = field(default_factory=list)
    triangles: List[Triangle] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        """Binary layout implementation."""
        # TODO: Implémenter
        return b""

    @classmethod
    def from_bytes(cls, data: bytes) -> "Triangles":
        """Deserialize Triangles from bytes."""
        # TODO: Implémenter
        raise NotImplementedError("Non implémenté")