from models.Point import Point
from models.PointSet import PointSet
from models.Triangle import Triangle
from models.Triangles import Triangles


def test_pointset_encode_decode():
    """Vérifie qu'un PointSet s'encode et se décode correctement selon la spec binaire.
    """
    pts = [Point(1.0, 2.0), Point(3.5, 4.5)]
    pset = PointSet(pts)

    binary = pset.to_bytes()

    # 4 bytes (nbr points) + 2 * 8 bytes (points) = 20 bytes
    assert len(binary) == 20, "La taille du binaire généré est incorrecte"

    decoded = PointSet.from_bytes(binary)

    assert len(decoded.points) == 2
    assert decoded.points[0].x == 1.0
    assert decoded.points[0].y == 2.0
    assert decoded.points[1].x == 3.5
    assert decoded.points[1].y == 4.5


def test_triangles_encode_decode():
    """Vérifie l'encodage complet : PointSet + Liste de Triangles.
    """
    pts = [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)]
    tris_list = [Triangle(0, 1, 2)]

    triangles_obj = Triangles(pts, tris_list)

    binary = triangles_obj.to_bytes()

    # Points : 4 (nbr points) + 3*8 (24) = 28 bytes
    # Triangles : 4 (nbr points) + 1*12 (12) = 16 bytes
    # Total = 44 bytes
    assert len(binary) == 44, "La taille du binaire Triangles est incorrecte"

    decoded = Triangles.from_bytes(binary)

    assert len(decoded.points) == 3
    assert len(decoded.triangles) == 1

    t = decoded.triangles[0]
    assert t.a == 0
    assert t.b == 1
    assert t.c == 2