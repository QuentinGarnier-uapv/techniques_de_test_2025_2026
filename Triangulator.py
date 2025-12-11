import urllib.request
import urllib.error
from models.PointSet import PointSet
from models.Point import Point
from models.Triangles import Triangles
from models.Triangle import Triangle


class Triangulator:
    def __init__(self):
        self.manager_url = "http://localhost:3000"

    def triangulate(self, pointSetId):
        """Orchestrateur (Service Layer)"""
        try:
            pset = self.get_point_set(pointSetId)
            result = self.compute(pset)
            return result.to_bytes()
        except Exception as e:
            raise e

    def get_point_set(self, pointSetId):
        # Basic UUID validation (length and hex) - simplified
        if len(pointSetId) != 36:
             raise Exception("incorrect uuid format")
        
        url = f"{self.manager_url}/pointset/{pointSetId}"
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                return PointSet.from_bytes(data)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise Exception("Point set not found")
            elif e.code == 503:
                raise Exception("point set manager unavailable")
            else:
                raise Exception(f"HTTP Error {e.code}")
        except urllib.error.URLError:
            raise Exception("point set manager unavailable")
        except Exception as e:
            raise e

    def compute(self, pset: PointSet) -> Triangles:
        """Algorithme de triangulation de Bowyer-Watson.
        Prend un PointSet en entrée et retourne un objet Triangles.
        """
        # Tri des points par ordre croissant de x => permet de gagner du temps dans le parcours des points (pas besoin de parcourir tous les triangles pour chaque point)
        points = sorted(pset.points, key=lambda p: p.x)
        
        n = len(points)
        if n < 3:
            return Triangles(points, [])
        
        # Super-triangle
        min_x = points[0].x
        max_x = points[-1].x
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)
        
        is_collinear = True
        p0 = points[0]
        p_end = points[-1]
        
        # c'est trié donc point 0 est le plus a gauche et point -1 est le plus a droite
        for p in points[1:-1]:
            if self.triangle_area(p0, p_end, p) > 1e-9:
                is_collinear = False
                break
        
        # si les extremités sont les memes points alors on a une droite car tout les points sont tres proches 
        if abs(max_x - min_x) < 1e-9 and abs(max_y - min_y) < 1e-9:
             is_collinear = True
             pass
        elif is_collinear:
             raise ValueError("Collinear points")

        dx = max_x - min_x
        # On definit le rectangle qui englobe tous les points
        dy = max_y - min_y
        delta_max = max(dx, dy)
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2
        
        # points du super triangle => 20 = augmentation superficielle pour assurer que le super triangle englobe tous les points
        st_p1 = Point(mid_x - 20 * delta_max, mid_y - delta_max)
        st_p2 = Point(mid_x + 20 * delta_max, mid_y - delta_max)
        st_p3 = Point(mid_x, mid_y + 20 * delta_max)
        
        # Ajout des points du super triangle a la liste des points
        all_points = points + [st_p1, st_p2, st_p3]
        
        # calcul du triangle super et de son cercle circonscrit
        t0 = Triangle(n, n+1, n+2)
        c0, r0_sq = self.get_circumcircle(st_p1, st_p2, st_p3)
        
        # liste des triangles actifs (triangles, centre_x, centre_y, rayon au carré)
        active_triangles = [(t0, c0[0], c0[1], r0_sq)]
        final_triangles = []

    def get_circumcircle(self, p1: Point, p2: Point, p3: Point):
        """Returns ((center_x, center_y), radius_sq)"""
        # https://en.wikipedia.org/wiki/Circumcircle pour la formule
        ax, ay = p1.x, p1.y
        bx, by = p2.x, p2.y
        cx, cy = p3.x, p3.y
        
        # determinant = 2 fois l'aire du triangle
        D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(D) < 1e-12:
            raise ValueError("Collinear points")

        # Coord du centre  
        ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / D
        uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / D
        
        # Rayon au carré : distance entre le centre et un des points
        r_sq = (ux - ax)**2 + (uy - ay)**2
        return (ux, uy), r_sq

    def triangle_area(self, p1, p2, p3):
        return 0.5 * abs(p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))