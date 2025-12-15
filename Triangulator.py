"""Module implementing the Triangulator service."""
import urllib.error
import urllib.request

from models.Point import Point
from models.PointSet import PointSet
from models.Triangle import Triangle
from models.Triangles import Triangles


class Triangulator:
    """Triangulator service implementation."""

    def __init__(self):
        """Initialize the triangulator."""
        self.manager_url = "http://localhost:3000"

    def triangulate(self, pointSetId):
        """Orchestrateur (Service Layer)."""
        try:
            pset = self.get_point_set(pointSetId)
            result = self.compute(pset)
            return result.to_bytes()
        except Exception:
            raise

    def get_point_set(self, pointSetId):
        """Get point set from manager by ID."""
        # Basic UUID validation (length and hex) - simplified
        if len(pointSetId) != 36:
             raise ValueError("incorrect uuid format")
        
        url = f"{self.manager_url}/pointset/{pointSetId}"
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return PointSet.from_bytes(data)


    def compute(self, pset: PointSet) -> Triangles:
        """Algorithme de triangulation de Bowyer-Watson.

        Prend un PointSet en entrée et retourne un objet Triangles.
        """
        # Tri des points par ordre croissant de x => permet de gagner du temps
        # dans le parcours des points (pas besoin de parcourir tous les triangles pour chaque point)
        points = sorted(pset.points, key=lambda p: p.x)
        
        n = len(points)
        if n < 3:
            return Triangles(points, [])
        
        self._check_collinearity(points)
        
        all_points, active_triangles = self._create_super_triangle(points)
        final_triangles = []
        
        for i, point in enumerate(points):
            bad_triangles, new_active_triangles, finished_triangles = self._find_bad_triangles(point, active_triangles)
            
            # Les triangles "finis" ne seront plus jamais affectés, on les stocke
            final_triangles.extend(finished_triangles)
            active_triangles = new_active_triangles
            
            polygon = self._find_hole_boundary(bad_triangles)
            
            self._fill_hole(polygon, i, all_points, active_triangles)
        
        # Ajoute les triangles restants a final
        for item in active_triangles:
             final_triangles.append(item[0])
                
        # Supprime les triangles connectés au super-triangle
        result_triangles = []
        for t in final_triangles:
            if t.a < n and t.b < n and t.c < n:
                result_triangles.append(t)
                
        return Triangles(points, result_triangles)

    def _check_collinearity(self, points):
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

    def _create_super_triangle(self, points):
        min_x = points[0].x
        max_x = points[-1].x
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)

        dx = max_x - min_x
        # On definit le rectangle qui englobe tous les points
        dy = max_y - min_y
        delta_max = max(dx, dy)
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2
        
        # points du super triangle => 20 = augmentation superficielle pour assurer que
        # le super triangle englobe tous les points
        st_p1 = Point(mid_x - 20 * delta_max, mid_y - delta_max)
        st_p2 = Point(mid_x + 20 * delta_max, mid_y - delta_max)
        st_p3 = Point(mid_x, mid_y + 20 * delta_max)
        
        # Ajout des points du super triangle a la liste des points
        all_points = points + [st_p1, st_p2, st_p3]
        
        # calcul du triangle super et de son cercle circonscrit
        n = len(points)
        t0 = Triangle(n, n+1, n+2)
        c0, r0_sq = self.get_circumcircle(st_p1, st_p2, st_p3)
        
        # liste des triangles actifs (triangle, centre_x, centre_y, rayon au carré)
        active_triangles = [(t0, c0[0], c0[1], r0_sq)]
        
        return all_points, active_triangles

    def _find_bad_triangles(self, point, active_triangles):
        bad_triangles = []
        new_active_triangles = []
        finished_triangles = []
        
        px, py = point.x, point.y
        
        for item in active_triangles:
            t, cx, cy, r_sq = item
            
            dx_dist = px - cx
            # Si le carré de la distance sur x est supérieur au rayon au carré
            # ET que le point est à droite du centre (dx_dist > 0),
            # alors on est sûr qu'aucun point futur ne tombera dans ce cercle.
            if dx_dist > 0 and (dx_dist**2) > r_sq:
                finished_triangles.append(t)
                continue
            
            # Si le point est dans le cercle, ce triangle sera 'mauvais'
            dist_sq = (cx - px)**2 + (cy - py)**2
            if dist_sq < r_sq:
                bad_triangles.append(t)
            else:
                new_active_triangles.append(item)
                
        return bad_triangles, new_active_triangles, finished_triangles

    def _find_hole_boundary(self, bad_triangles):
        # polygon = frontiére du polygone formé par bad_triangles
        # Trouve la frontière du polygone formé par bad_triangles
        # Utilise un dictionnaire pour compter les arêtes: (min, max) -> count
        edge_counts = {}
        for t in bad_triangles:
            for edge in [(t.a, t.b), (t.b, t.c), (t.c, t.a)]:
                sorted_edge = tuple(sorted(edge))
                # On compte le nombre d'occurences de chaque arete
                # (arrete comptée 2 fois si elle est partagée par 2 triangles /
                # arrete comptée 1 fois si elle est frontière)
                edge_counts[sorted_edge] = edge_counts.get(sorted_edge, 0) + 1
        
        polygon = [edge for edge, count in edge_counts.items() if count == 1]
        return polygon

    def _fill_hole(self, polygon, point_index, all_points, active_triangles):
        # Re-triangule le trou
        for edge in polygon:
            new_t = Triangle(edge[0], edge[1], point_index)
            p1 = all_points[new_t.a]
            p2 = all_points[new_t.b]
            p3 = all_points[new_t.c]
            
            try:
                center, r_sq = self.get_circumcircle(p1, p2, p3)
                active_triangles.append((new_t, center[0], center[1], r_sq))
            except ValueError:
                 continue

    def get_circumcircle(self, p1: Point, p2: Point, p3: Point):
        """Return ((center_x, center_y), radius_sq)."""
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
        """Calculate the area of the triangle formed by p1, p2, p3."""
        return 0.5 * abs(
            p1.x * (p2.y - p3.y) +
            p2.x * (p3.y - p1.y) +
            p3.x * (p1.y - p2.y)
        )