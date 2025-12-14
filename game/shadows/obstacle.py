class Obstacle:
    def __init__(self, corners, polygon):
        self.corners = corners
        self.polygon = polygon
        self.distance = 0
        center = list(self.polygon.centroid.coords)[0]
        self.center = (int(center[0]), int(center[1]))