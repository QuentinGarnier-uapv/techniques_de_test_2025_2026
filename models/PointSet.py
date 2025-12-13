"""Module handling PointSet data model."""
import struct
from dataclasses import dataclass, field

from .Point import Point

# note formatage : < => little-endian (octet de poids faible en premier), I => unsigned int (4 bytes)


@dataclass
class PointSet:
    """Represent a set of points."""

    points: list[Point] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        """Format: 4 bytes unsigned int count + each point (8 bytes)."""
        header = struct.pack("<I", len(self.points))
        body = b""
        for p in self.points:
            body += p.to_bytes()
        return header + body

    @classmethod
    def from_bytes(self, data: bytes) -> "PointSet":
        """Parse PointSet from bytes."""
        if len(data) < 4:
            raise ValueError("Data too short")
        
        count = struct.unpack("<I", data[:4])[0]
        points = []
        offset = 4
        
        for _ in range(count):
            if offset + 8 > len(data):
                raise ValueError("Data too short for points")
            bytePoint = data[offset : offset + 8]
            points.append(Point.from_bytes(bytePoint))
            offset += 8
            
        return self(points=points)