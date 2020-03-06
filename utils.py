# coding: utf8

import numpy as np


# PARTIE 1 : DISCRETISATION DE LA TRAJECTOIRE #

def init_sommets(dimensions):
    lx, ly, lz = dimensions
    return np.array([[lx/2, -ly/2, -lz/2],
                     [lx/2, -ly/2, lz/2],
                     [lx/2, ly/2, -lz/2],
                     [lx/2, ly/2, lz/2],
                     [-lx/2, ly/2, -lz/2],
                     [-lx/2, ly/2, lz/2],
                     [-lx/2, -ly/2, -lz/2],
                     [-lx/2, -ly/2, lz/2]])


def pos_to_sommets(position, dimensions):
    sommets = init_sommets(dimensions)
    for sommet in range(8):
        sommets[sommet] = np.dot(rotation(position.angle), sommets[sommet])\
                          + position.spatial
    return sommets


def rotation(angular_vect):
    rho = angular_vect[0]
    theta = angular_vect[1]
    phi = angular_vect[2]

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
