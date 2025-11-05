from dataclasses import dataclass, field
from typing import List
import struct
from .Point import Point
from .Triangle import Triangle
from .PointSet import PointSet

@dataclass
class Triangles:
    points: List[Point] = field(default_factory=list)
    triangles: List[Triangle] = field(default_factory=list)

    def to_bytes(self) -> bytes | None:
        """
        Binary layout:
        - vertices part: same as PointSet (4 bytes count + points)
        - triangles part: 4 bytes count + 3*4 bytes per triangle
        """
        return None

    @classmethod
    def from_bytes(cls, data: bytes) -> "Triangles | None":
        """Deserialize Triangles from bytes according to spec."""
        return None

