# coding: utf8


# 1. DISCRETISATION

def calcul_pas_adapte(trajectoire, pas_maximal):
    print(trajectoire)
    print(pas_maximal)
    pass


def discretisation_trajectoire(trajectoire, pas_maximal):
    print(trajectoire)
    print(pas_maximal)
    calcul_pas_adapte(trajectoire, pas_maximal)
    pass


# 2. LONGUEUR DES CABLES

def pos_to_cable_length(position):
    print(position)
    pass


def get_cable_var(mobile, trajectoire_disc, dimensions):
    print(trajectoire_disc)
    print(dimensions)
    for position in trajectoire_disc:
        mobile.move(position)
        pos_to_cable_length(position)
    pass
