# coding: utf8

from utils import rotation, init_sommets


class Mobile:

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.position = Coord6d()
        self.sommets = init_sommets(self.dimensions)

    def move(self, spatial, angular):
        self.change_spatial(spatial)
        self.change_angular(angular)
        pass


class Hangar:

    def __init__(self):
        pass


class Coord6d:

    def __init__(self, x=0, y=0, z=0, alpha=0, beta=0, gamma=0):
        self.spatial = [x, y, z]
        self.angle = [alpha, beta, gamma]

    def change_spatial(self, spatial):
        pass

    def change_angular(self, angular):
        rotation(angular)
        pass


