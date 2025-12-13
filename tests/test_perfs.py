import random
import time

import pytest

from models.Point import Point
from models.PointSet import PointSet
from Triangulator import Triangulator

# Applique le marqueur 'performance' à tous les tests de ce fichier
pytestmark = pytest.mark.performance

tri = Triangulator()


def generate_pointset(size: int, distribution: str, amplitude: tuple = (0, 1000)) -> PointSet:
    """Génère un PointSet selon une distribution spécifique.
    Inspiré par la logique fournie, corrigée pour la syntaxe.
    """
    min_val, max_val = amplitude
    points = []

    match distribution:
        case "uniform":
            # x = U(min_val, max_val), y = U(min_val, max_val)
            points = [
                Point(random.uniform(min_val, max_val), random.uniform(min_val, max_val))
                for _ in range(size)
            ]
        case "linear":
            # y = m * x, avec m = 1.5
            # x = U(min_val, max_val)
            points = []
            for _ in range(size):
                x = random.uniform(min_val, max_val)
                y = x * 1.5
                points.append(Point(x, y))

        case "clustered":
            # 5 centres denses (simule des villes sur une carte).
            # j'utilise les "Gaussian Blob" que j'ai déciouvert ici https://www.geeksforgeeks.org/python/random-gauss-function-in-python/
            centers = [
                (random.uniform(min_val, max_val), random.uniform(min_val, max_val))
                for _ in range(5)
            ]
            ecart_t = (max_val - min_val) / 20

            for _ in range(size):
                cx, cy = random.choice(centers)
                px = cx + random.gauss(0, ecart_t)
                py = cy + random.gauss(0, ecart_t)
                points.append(Point(px, py))

        case _:
            raise ValueError(f"Distribution inconnue: {distribution}")

    return PointSet(points)


@pytest.mark.parametrize("Amplitude", [(0, 10), (0, 100), (0, 1000)])
@pytest.mark.parametrize("size", [100, 1000, 5000])
@pytest.mark.parametrize("distribution", ["uniform", "linear", "clustered"])
def test_perf_triangulation_compute(size, distribution, Amplitude):
    """Mesure le temps de calcul pur de la triangulation.
    """
    pset = generate_pointset(size, distribution, amplitude=Amplitude)

    start_time = time.time()
    if distribution == "linear":
        with pytest.raises(ValueError, match="Collinear points"):
            tri.compute(pset)
    else:
        tri.compute(pset)
    end_time = time.time()

    duration = end_time - start_time
    print(f"\n[Triangulation] {size} points ({distribution}, Amp={Amplitude}) : {duration:.4f}s")

@pytest.mark.parametrize("size", [1000, 10000])
def test_perf_binary_encoding(size):
    """Mesure le temps de conversion en binaire (To Bytes).
    La distribution importe peu ici, c'est le volume qui compte.
    """
    pset = generate_pointset(size, "uniform")

    start_time = time.time()
    _ = pset.to_bytes()
    end_time = time.time()

    duration = end_time - start_time
    print(f"\n[Encoding] {size} points : {duration:.4f}s")