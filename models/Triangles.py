from dataclasses import dataclass, field
import struct

from .Point import Point
from .PointSet import PointSet
from .Triangle import Triangle


@dataclass
class Triangles:
    points: list[Point] = field(default_factory=list)
    triangles: list[Triangle] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        """Binary layout implementation."""     
        ps_bytes = PointSet(self.points).to_bytes()
        tris_header = struct.pack("<I", len(self.triangles))
        tris_body = b"".join(t.to_bytes() for t in self.triangles)
        return ps_bytes + tris_header + tris_body

    @classmethod
    def from_bytes(self, data: bytes) -> "Triangles":
        """Deserialize Triangles from bytes."""
        if len(data) < 4:
            raise ValueError("Data too short")
        
        ps_count = struct.unpack("<I", data[:4])[0]
        ps_size = 4 + ps_count * 8
        if len(data) < ps_size:
            raise ValueError("Data too short for PointSet")
        
        ps_data = data[:ps_size]
        ps = PointSet.from_bytes(ps_data)
        offset = ps_size
        if len(data) < offset + 4:
            raise ValueError("Data too short for Triangle count")
        
        t_count = struct.unpack("<I", data[offset:offset+4])[0]
        offset += 4
        t_size = 12
        triangles = []
        for _ in range(t_count):
            if offset + t_size > len(data):
                raise ValueError("Data too short for expected triangles")
            triangle = data[offset : offset + t_size]
            triangles.append(Triangle.from_bytes(triangle))
            offset += t_size
        return self(points=ps.points, triangles=triangles)