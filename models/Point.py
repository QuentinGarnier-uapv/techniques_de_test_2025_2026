from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def to_bytes(self) -> bytes:
        """Serialize as two 4-byte floats (little-endian)."""
        # TODO: Implémenter la conversion
        return b""

    @classmethod
    def from_bytes(cls, b: bytes) -> "Point":
        """Deserialize 8 bytes into a Point."""
        # TODO: Implémenter la lecture
        # On retourne un point par défaut ou on laisse planter le test proprement
        raise NotImplementedError("La méthode from_bytes n'est pas encore implémentée")

    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)