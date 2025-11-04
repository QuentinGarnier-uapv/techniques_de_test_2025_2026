class Triangulator:
    def __init__(self):
        pass

    def triangulate(self, pointSetId):
        try:
            get_point_set = self.get_point_set(pointSetId)
            return []
        except Exception as e:
            raise e

    def get_point_set(self, pointSetId):
        print("real get_point_set called")
        return None