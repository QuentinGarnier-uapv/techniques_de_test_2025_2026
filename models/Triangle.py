from dataclasses import dataclass

@dataclass
class Triangle:
    a: int
    b: int
    c: int

    def to_bytes(self) -> bytes:
        """Serialize as three unsigned 4-byte integers (little-endian)."""
        # TODO: Implémenter
        return b""

    @classmethod
    def from_bytes(cls, b: bytes) -> "Triangle":
        # TODO: Implémenter
        raise NotImplementedError("Non implémenté")