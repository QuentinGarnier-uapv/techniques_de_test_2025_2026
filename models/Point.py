"""Module handling Point data model."""
import struct
from dataclasses import dataclass

# note formatage : <ff => little-endian (octet de poids faible en premier),
# 2 floats (32 bits chacun) => perte de précision car en python floats de 64 bits


@dataclass
class Point:
    """Represent a 2D point with x and y coordinates."""

    x: float
    y: float

    def to_bytes(self) -> bytes:
        """Serialize as two 4-byte floats (little-endian)."""
        return struct.pack("<ff", self.x, self.y)

    @classmethod
    def from_bytes(cls, b: bytes) -> "Point":
        """Deserialize 8 bytes into a Point."""
        try:
            x, y = struct.unpack("<ff", b)
            return cls(x, y)
        except struct.error as e:
            raise ValueError("Invalid byte sequence for Point") from e

    def to_tuple(self) -> tuple[float, float]:
        """Convert point to a tuple of (x, y)."""
        return (self.x, self.y)