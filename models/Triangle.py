# python
from dataclasses import dataclass
import struct

@dataclass
class Triangle:
    a: int
    b: int
    c: int

    def to_bytes(self) -> bytes | None:
        """Serialize as three unsigned 4-byte integers (little-endian)."""
        return None

    @classmethod
    def from_bytes(cls, b: bytes) -> "Triangle | None":
        """Deserialize 12 bytes into a Triangle."""
        return None
