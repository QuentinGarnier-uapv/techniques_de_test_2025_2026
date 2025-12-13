"""Module handling Triangle data model."""
import struct
from dataclasses import dataclass


@dataclass
class Triangle:
    """Represent a triangle by 3 indices to points."""

    a: int
    b: int
    c: int

    def to_bytes(self) -> bytes:
        """Format: 3*4 bytes unsigned int."""
        return struct.pack("<III", self.a, self.b, self.c)

    @classmethod
    def from_bytes(self, data: bytes) -> "Triangle":
        """Deserialize Triangle from bytes."""
        if len(data) < 12:
            raise ValueError("Invalid byte sequence for Triangle")
        try:
            a, b, c = struct.unpack("<III", data)
            return self(a, b, c)
        except struct.error as e:
            raise ValueError("Invalid byte sequence for Triangle") from e