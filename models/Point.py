# python
from dataclasses import dataclass
import struct
from typing import Tuple

@dataclass
class Point:
    x: float
    y: float

    def to_bytes(self) -> bytes | None:
        """Serialize as two 4-byte floats (little-endian)."""
        return None

    @classmethod
    def from_bytes(cls, b: bytes) -> "Point | None":
        """Deserialize 8 bytes into a Point."""
        return None

    def to_tuple(self) -> Tuple[float, float]:
        """Return point as (x, y) tuple."""
        return (self.x, self.y)
