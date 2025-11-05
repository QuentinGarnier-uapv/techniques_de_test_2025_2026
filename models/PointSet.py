# python
from dataclasses import dataclass, field
from typing import List
import struct
from .Point import Point

@dataclass
class PointSet:
    points: List[Point] = field(default_factory=list)

    def to_bytes(self) -> bytes| None:
        """Format: 4 bytes unsigned int count + each point (8 bytes)."""
        return None

    @classmethod
    def from_bytes(cls, data: bytes) -> "PointSet | None":
        """
        Parse PointSet from bytes. Expects at least 4 bytes for count,
        then count * 8 bytes for points.
        """
        return None
