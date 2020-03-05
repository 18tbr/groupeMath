# coding: utf8

import numpy as np


def init_sommets(lx, ly, lz):
    return np.array([[lx/2, -ly/2, -lz/2],
                     [lx/2, -ly/2, lz/2],
                     [lx/2, ly/2, -lz/2],
                     [lx/2, ly/2, lz/2],
                     [-lx/2, ly/2, -lz/2],
                     [-lx/2, ly/2, lz/2],
                     [-lx/2, -ly/2, -lz/2],
                     [-lx/2, -ly/2, lz/2]])


def pos_to_sommets(position, dimensions):
    sommets = init_sommets(dimensions[0], dimensions[1], dimensions[2])
    for sommet in range(8):
        sommets[sommet] = np.dot(rotation(position.angle), sommets[sommet])\
                          + position.spatial
    return sommets


def rotation(vecteur_rotation):
    rho = vecteur_rotation[0]
    theta = vecteur_rotation[1]
    phi = vecteur_rotation[2]

    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rho), np.sin(rho)],
                   [0, -np.sin(rho), np.cos(rho)]])

    Ry = np.array([[np.cos(theta), 0, -np.sin(theta)],
                   [0, 1, 0],
                   [np.sin(theta), 0, np.cos(theta)]])

    Rz = np.array([[np.cos(phi), np.sin(phi), 0],
                   [-np.sin(phi), np.cos(phi), 0],
                   [0, 0, 1]])

    return np.dot(np.dot(Rx, Ry), Rz)


class Mobile:

    def __init__(self, lx, ly, lz):
        self.dimensions = [lx, ly, lz]
        self.position = Coord6d()
        self.sommets = pos_to_sommets(self.position, self.dimensions)

    def move(self, x, y, z, alpha, beta, gamma):
        self.position.change_coord(x, y, z, alpha, beta, gamma)
        self.sommets = pos_to_sommets(self.position, self.dimensions)


class Hangar:

    def __init__(self):
        pass


class Coord3d:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Coord6d:

    def __init__(self, x=0, y=0, z=0, alpha=0, beta=0, gamma=0):
        self.spatial = [x, y, z]
        self.angle = [alpha, beta, gamma]

    def change_coord(self, x, y, z, alpha, beta, gamma):
        self.spatial = [x, y, z]
        self.angle = [alpha, beta, gamma]


if __name__ == "__main__":
    mobile = Mobile(1, 2, 3)
    print(mobile.position.spatial)
    print(mobile.position.angle)
    mobile.move(1, 1, 1, 0, 0, 0)
    print(mobile.position.spatial)
    print(mobile.position.angle)
