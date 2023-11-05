class Coords:
    def __init__(self, id):
        self.id = id


class Route:
    def __init__(self, route=None):
        if route is None:
            route = []
        self.route = route
        self.distance = 0