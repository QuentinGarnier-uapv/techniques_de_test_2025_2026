from dataclasses import dataclass
import struct

@dataclass
class Triangle:
    a: int
    b: int
    c: int

    def to_bytes(self) -> bytes:
        """Format: 3*4 bytes unsigned int."""
        return struct.pack("<III", self.a, self.b, self.c)

    @classmethod
    def from_bytes(self, data: bytes) -> "Triangle":
        if len(data) < 12:
            raise ValueError("Invalid byte sequence for Triangle")
        try:
            a, b, c = struct.unpack("<III", data)
            return self(a, b, c)
        except struct.error as e:
            raise ValueError("Invalid byte sequence for Triangle") from e