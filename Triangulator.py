from models.PointSet import PointSet
from models.Triangles import Triangles


class Triangulator:
    def __init__(self):
        pass

    def triangulate(self, pointSetId):
        """Orchestrateur (Service Layer)"""
        try:
            pset = PointSet([])

            result = self.compute(pset)

            return result.to_bytes()
        except Exception as e:
            raise e

    def compute(self, pset: PointSet) -> Triangles:
        """
        Algorithme de triangulation.
        Prend un PointSet en entrée et retourne un objet Triangles.
        """
        return Triangles(points=pset.points, triangles=[])

    def get_point_set(self, pointSetId):
        print("real get_point_set called")
        return None