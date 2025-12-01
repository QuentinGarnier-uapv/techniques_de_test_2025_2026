from dataclasses import dataclass, field

from .Point import Point
from .Triangle import Triangle


@dataclass
class Triangles:
    points: list[Point] = field(default_factory=list)
    triangles: list[Triangle] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        """Binary layout implementation."""
        # TODO: Implémenter
        return b""

    @classmethod
    def from_bytes(cls, data: bytes) -> "Triangles":
        """Deserialize Triangles from bytes."""
        # TODO: Implémenter
        raise NotImplementedError("Non implémenté")