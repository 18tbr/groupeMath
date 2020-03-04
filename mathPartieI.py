# coding: utf8

# On suppose que l'on a une série de points en entrée, on s'occupera
# de ce détail plus tard.
# On considère le pas de temps comme imposé dans la cadre arduino

import numpy as np
import math
from pylab import *

############### Première partie : Discrétisation de la trajectoire ############

# 3 longeurs en m
pas_translation_x = 0.01
pas_translation_y = 0.01
pas_translation_z = 0.01
# 3 angles en radian
pas_rotation_alpha = 3.14/180
pas_rotation_beta = 3.14/180
pas_rotation_gamma = 3.14/180
# vecteur des pas maximaux que l'on s'autorise
pas_maximal = np.array([pas_translation_x, pas_translation_y,
                        pas_translation_z, pas_rotation_alpha,
                        pas_rotation_beta, pas_rotation_gamma])


def calcul_pas_adapte(trajectoire, pas_maximal):
    """
    Donne le nombre de pas à effectuer pour chaque dimension pour une étape
    dans la trajectoire.

    Pour calculer le pas adapté, on calcule le nombre de pas minimal que l'on
    devra faire pour aller de la source à la destination (la dimension dont le
    pas est le plus petit dicte le nombre de pas).

    :param trajectoire: Trajectoire souhaitée
    :param pas_maximal: vecteur de taille 6 des pas maximaux

    :type trajectoire: np.array
    :type pas_maximal: np.array de taille 6

    :return: Vecteur de taille 9 des pas pour chaque intervalle
    :rtype: np.array
    """

    nb_intervalles = len(trajectoire) - 1
    nombre_pas = np.zeros(nb_intervalles, dtype=int)

    for j in range(nb_intervalles):
        nombre_pas_detail = np.zeros(6)
        for i in range(6):
            nombre_pas_detail[i] = abs(trajectoire[j+1][i] -
                                       trajectoire[j][i]) / pas_maximal[i]
        nombre_pas[j] = math.ceil(np.amax(nombre_pas_detail))
    return nombre_pas


trajectoire = np.random.rand(10, 6)
# print("Trajectoire :\n", trajectoire)
# print(calcul_pas_adapte(trajectoire, pas_maximal))


def discretisation_trajectoire(trajectoire, pas_maximal):
    """
    Discrétise la trajectoire souhaitée en divisant les parties trop grandes en
    pas de longueurs constantes par morceaux plus petits que pas_maximal.
    Renvoie 2 listes :
    1. la liste des points par lesquels il faut passer, inutile pour les
    moteurs mais utile pour tracer les courbes de trajectoire ;
    2. la liste des déplacements infinitésimaux qu'il faut pour passer d'un
    point à un autre. Chacun de ces déplacements infintésimaux est un np.arra
    de 6 dimensions, 3 en position et 3 angulaires.

    :param trajectoire: Trajectoire souhaitée
    :param pas_maximal: vecteur de taille 6 des pas maximaux

    :type trajectoire: np.array
    :type pas_maximal: np.array de taille 6

    :return: Couple d'arrays
    :rtype: (np.array, np.array)
    """

    nb_intervalles = len(trajectoire) - 1
    nombre_pas = calcul_pas_adapte(trajectoire, pas_maximal)

    traj_disc = np.zeros((1, 6))
    var_disc = np.zeros((1, 6))
    # traj_disc = np.empty((1, 6))
    # var_disc = np.empty((1, 6))

    for j in range(nb_intervalles):
        nb_pas_j = nombre_pas[j]

        dx = (trajectoire[j+1][0] - trajectoire[j][0]) / nb_pas_j
        dy = (trajectoire[j+1][1] - trajectoire[j][1]) / nb_pas_j
        dz = (trajectoire[j+1][2] - trajectoire[j][2]) / nb_pas_j
        dalpha = (trajectoire[j+1][3] - trajectoire[j][3]) / nb_pas_j
        dbeta = (trajectoire[j+1][4] - trajectoire[j][4]) / nb_pas_j
        dgamma = (trajectoire[j+1][5] - trajectoire[j][5]) / nb_pas_j

        for i in range(0, nb_pas_j):
            x = trajectoire[j][0] + i * dx
            y = trajectoire[j][1] + i * dy
            z = trajectoire[j][2] + i * dz
            alpha = trajectoire[j][3] + i * dalpha
            beta = trajectoire[j][4] + i * dbeta
            gamma = trajectoire[j][5] + i * dgamma

            traj_disc = np.append(traj_disc,
                                  [[x, y, z, alpha, beta, gamma]],
                                  axis=0)
            var_disc = np.append(var_disc,
                                 [[dx, dy, dz, dalpha, dbeta, dgamma]],
                                 axis=0)

    return traj_disc, var_disc

# Test of discretisation_trajectoire
# [trj, var] = discretisation_trajectoire(trajectoire, pas_maximal)


discretisation_trajectoire(trajectoire, pas_maximal)


##################### Deuxième partie : Longueur des câbles ####################

# Convertit les déplacements infintésimaux du mobile en variations de longueurs
# des câbles en utilisant des matrices de rotation.


def construction_mobile(dimensions):
    """
    Renvoie la liste de taille 8 des coordonnées des points du mobile ; chaque
    coordonnée de coin du rectangle sera un array de taille 3 (x, y et z).
    Attention, les croisements ne sont pas pris en compte.

    :param dimensions: dimensions physiques du mobile que l'on souhaite
    construire, array de dimension 3 (x, y et z)

    :type dimensions: np.array

    :return: liste de taille 8 des coordonnées des points du mobile
    :rtype: np.array
    """
    lx = dimensions[0]
    ly = dimensions[1]
    lz = dimensions[2]

    A6 = np.array([-lx/2, -ly/2, -lz/2])
    A7 = np.array([-lx/2, -ly/2, lz/2])
    A5 = np.array([-lx/2, ly/2, lz/2])
    A4 = np.array([-lx/2, ly/2, -lz/2])
    A0 = np.array([lx/2, -ly/2, -lz/2])
    A1 = np.array([lx/2, -ly/2, lz/2])
    A3 = np.array([lx/2, ly/2, lz/2])
    A2 = np.array([lx/2, ly/2, -lz/2])

    mobile = [A0, A1, A2, A3, A4, A5, A6, A7]
    return mobile


def construction_hangar(dimensions):
    """
    Renvoie la liste de taille 8 des coordonnées des points du hangar ; chaque
    coordonnée de coin du rectangle est un array de taille 3 (x, y et z).
    Le coin A6 doit être placé à l'origine.

    :param dimensions: dimensions physiques du hangar que l'on souhaite
    construire, array de dimension 3 (x, y et z)

    :type trajectoire: np.array

    :return: liste de taille 8 des coordonnées des points du hangar
    :rtype: np.array
    """
    lx = dimensions[0]
    ly = dimensions[1]
    lz = dimensions[2]

    A6 = np.array([0, 0, 0])
    A7 = np.array([0, 0, lz])
    A5 = np.array([0, ly, lz])
    A4 = np.array([0, ly, 0])
    A0 = np.array([lx, 0, 0])
    A1 = np.array([lx, 0, lz])
    A3 = np.array([lx, ly, lz])
    A2 = np.array([lx, ly, 0])

    hangar = [A0, A1, A2, A3, A4, A5, A6, A7]
    return hangar


def construction_rectangle(dimensions, centre):
    # à supprimer

    # dimensions contient les dimensions physiques du pavé que l'on souhaite
    # construire. Il s'agit d'un np.array de dimension 3 (x, y et z).
    # centre est un booleen qui indique si l'on doit placer le centre du
    # rectangle sur l'origine ou plutôt le coin A6. True signifie que le centre
    # doit être placé à l'origine (pour le mobile) et False signifie que le
    # coin A6 doit être placé à l'origine.

    # Cette fonction annexe mais utile est celle que vous avez défini dans
    # votre code comme coinHangar. Je pense qu'elle va effectivement vous permettre
    # d'avoir un code plus simple à lire.

    # Cette fonction renvoie une liste de taille 8 des coordonnées des points
    # du rectangle collé contre l'origine et orienté comme le hangar. Chaque
    # coordonnée de coin du rectangle sera un np.array de dimension 3 (x, y et z)
    lx = dimensions[0]
    ly = dimensions[1]
    lz = dimensions[2]

    if centre: # attention, croisement pas pris en compte
        A6 = np.array([-lx/2, -ly/2, -lz/2])
        A7 = np.array([-lx/2, -ly/2, lz/2])
        A5 = np.array([-lx/2, ly/2, lz/2])
        A4 = np.array([-lx/2, ly/2, -lz/2])
        A0 = np.array([lx/2, -ly/2, -lz/2])
        A1 = np.array([lx/2, -ly/2, lz/2])
        A3 = np.array([lx/2, ly/2, lz/2])
        A2 = np.array([lx/2, ly/2, -lz/2])

    else:
        A6 = np.array([0, 0, 0])
        A7 = np.array([0, 0, lz])
        A5 = np.array([0, ly, lz])
        A4 = np.array([0, ly, 0])
        A0 = np.array([lx, 0, 0])
        A1 = np.array([lx, 0, lz])
        A3 = np.array([lx, ly, lz])
        A2 = np.array([lx, ly, 0])
    mobile = [A0, A1, A2, A3, A4, A5, A6, A7]
    return mobile


def rotation(vecteur_rotation):
    """
    Renvoie la matrice de rotation associée aux angles de rotation.
    Multiplier un vecteur par la matrice de rotation permettra de lui faire
    subir les trois rotations.

    :param vecteur_rotation: vecteur des 3 angles de rotation.
    rho, theta et phi sont des déplacements angulaires du mobile autour des
    trois vecteurs de la base du hangar.

    :type vecteur_rotation: np.array de taille 3

    :return: produit des trois matrices de rotations données respectivement
    par les angles rho, theta, et phi
    :rtype: np.array de dimension 3x3
    """
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


def reconstruction_coins(position_mobile, dimensions_mobile):
    """
    Calcule la liste des positions des 8 coins du mobile à partir des
    dimensions et des coordonnées du centre du mobile.
    Renvoie la liste des positions des 8 coins. Chaque position est un
    np.array de taille 3 (x, y, z).
    On appelle cette fonction à chaque fois que l'on change les
    coordonnées du mobile.
    Méthode :
    1. Création du mobile de bonnes dimensions mais en faisant coincider le
    centre du mobile avec le centre du repère du hangar ;
    2. Orientation du mobile pour qu'il soit aligné avec l'orientation donnée
    par base_mobile (en utilisant des matrices de rotation pour arriver à

    #######################################
    ##### Qu'est ce que base_mobile ? #####
    #######################################

    l'orientation souhaitée depuis l'orientation d'origine du hangar) ;
    3. Déplacement du mobile pour que son centre se retrouve à la position
    donnée par position_mobile.

    A faire : passer mobile en argument ?

    :param position_mobile: np.array de taille 6 (3 positions, 3 angles)
    représentant la position actuelle du centre du mobile et son orientation.
    :param dimensions_mobile: np.array de taille 3 (longueur, largeur, hauteur)

    :type position_mobile: np.array de taille 6
    :type dimensions_mobile: np.array de taille 3

    :return: liste de 8 éléments des positions des huits coins
    :rtype: liste
    """

    # 1.
    mobile = construction_mobile(dimensions_mobile)

    # 2
    orientation = position_mobile[3:6]
    rotation_mobile = rotation(orientation)

    # 3
    translationCentre = position_mobile[0:3]

    for coord in range(8):
        mobile[coord] = np.dot(rotation_mobile, mobile[coord])  # 2
        mobile[coord] += translationCentre  # 3

    return mobile


def calcul_longueurs_cables(pos_coins_mobile, pos_coins_hangar):
    """
    Renvoie les longueurs des 8 câbles correspondant à la position du mobile
    dans le hangar.
    Les câbles étant croisés dans le hangar, on introduit en (a) une liste de
    changements d'indices.

    :param pos_coins_mobile: liste des positions des 8 coins du mobile, chaque
    position étant un np.array de taille 3 (x, y, z) dans l'ordre de la
    numérotation donnée sur le schéma.
    :param pos_coins_hangar: liste des positions des 8 coins du hangar, chaque
    position étant un np.array de taille 3 (x, y, z) dans l'ordre de la
    numérotation donnée sur le schéma.

    #########################
    ##### Quel schéma ? #####
    #########################

    :type pos_coins_mobile: np.array
    :type pos_coins_hangar: np.array

    :return: vecteur des longueurs des 8 câbles
    :rtype: np.array de taille 8
    """

    longueurCable = np.zeros(8)
    # (a)
    chgt_num = [6, 7, 4, 5, 2, 3, 0, 1]

    for cable in range(8):
        vecteurCoins = pos_coins_mobile[chgt_num[cable]] - pos_coins_hangar[cable]
        longueurCable[cable] = np.linalg.norm(vecteurCoins)

    return longueurCable


def commande_longeurs_cables(trajectoire_discretisee, dimensions_physiques_mobile, dimensions_physiques_hangar):
    # Cette fonction prend en argument la trajectoire discrétisée dans la première partie du code, chaque point de la trajectoire étant un np.array de dimension 6, 3positions + 3 angles.
    # dimensions_physiques_mobile est cohérent avec la définition donnée dans reconstruction_coins.
    # dimensions_physiques_hangar est défini comme dimensions_physiques_mobile mais pour le hangar.

    # Cette fonction va prendre en argument la trajectoire discrétisée, i.e. la liste des déplacements infintésimaux qu'il faut réaliser pour parcourir la trajectoire souhaitée, et va la convertir en une liste de modifications infintésimales des longueurs de corde.
    # Pour cela, on doit garder en mémoire (dans des variables locales) la position actuelle du module (np.array de 6 dimensions, 3 positions + 3 angles) ainsi que les longueurs actuelles des cordes (un np.array de dimension 8).

    # Pour chaque déplacement infintésimal dans cette boucle on devra :
    # - 1 : Mettre à jour la position mémorisée du mobile (selon les 6 dimensions).
    # - 2 : Reconstruire les coins du mobile (en prenant en compte l'orientation avec reconstruction_coins).
    # - 3 : Calculer les nouvelles longueurs des cordes.
    # - 4 : En déduire les variations des longueurs des cordes par rapport à celles de l'état précédent.
    # - 5 : Mettre à jour les longueurs des cordes.

    # Cette fonction renverra un liste des modifications de longueurs des cordes, chaque élément de la liste étant un np.array de dimension 8 dont le ième élément est la variation de longueur de la ième corde.
    coinsHangar = construction_hangar(dimensions_physiques_hangar)

    nombreIteration = len(trajectoire_discretisee[1]) ## obj nombre de pas total
    positionInitiale = trajectoire_discretisee[0][0]  ### ATTENTION JE NE SAIS PAS SI CA FONCTIONNE ET C'EST UN DETAIL IMPORTANT
    coinsPositionInit = reconstruction_coins(positionInitiale, dimensions_physiques_mobile)

    longueursCableInit = calcul_longueurs_cables(coinsPositionInit, coinsHangar)
    tableauVarLongueur = []
    tableauLongueur = []  # test
    for n in range(1, nombreIteration):

        nouvellePosition = positionInitiale + trajectoire_discretisee[1][n]
        coinsNouvellePosition = reconstruction_coins(nouvellePosition, dimensions_physiques_mobile)
        nouvellesLongueursCables = calcul_longueurs_cables(coinsNouvellePosition, coinsHangar)
        variationLongueur = nouvellesLongueursCables-longueursCableInit
        tableauVarLongueur += [variationLongueur]
        tableauLongueur += [nouvellesLongueursCables] ##test
        longueursCableInit = nouvellesLongueursCables
        positionInitiale = nouvellePosition

    return [tableauVarLongueur, tableauLongueur]  # on retourne une liste des variations de longueur des cables


# Definir la trajectoire
origine = np.array([0, 0, 0, 0, 0, 0])
destination = np.array([0.5, 0.5, 0.5, 0, 0, 0])

# trajectoire = np.array([origine], dtype=float)
# trajectoire = np.insert(trajectoire, 1, destination, 0)
trajectoire = np.random.rand(10, 6)

centre = np.array([0, 0, 0, 0, 0, 0])
dimension = np.array([0.25, 0.25, 0.3])
coinsMobile = (reconstruction_coins(centre, dimension))


dimensionHangar = np.array([1.25, 1.25, 1])
coinsHangar = construction_hangar(dimensionHangar)
print(calcul_longueurs_cables(coinsMobile, coinsHangar))

varlongueurCable, longueurCable = commande_longeurs_cables(discretisation_trajectoire(trajectoire, pas_maximal), dimension, dimensionHangar)


var0 = []
var1 = []
var2 = []
var3 = []
var4 = []
var5 = []
var6 = []
var7 = []

n = len(varlongueurCable)
print(n)

for i in range(n):
    var0.append(varlongueurCable[i][0])
    var1.append(varlongueurCable[i][1])
    var2.append(varlongueurCable[i][2])
    var3.append(varlongueurCable[i][3])
    var4.append(varlongueurCable[i][4])
    var5.append(varlongueurCable[i][5])
    var6.append(varlongueurCable[i][6])
    var7.append(varlongueurCable[i][7])

subplot(1, 2, 1)

x = list(range(n))
plot(x, var0, label='Cable 0')
plot(x, var1, label='Cable 1')
plot(x, var2, label='Cable 2')
plot(x, var3, label='Cable 3')
plot(x, var4, label='Cable 4')
plot(x, var5, label='Cable 5')
plot(x, var6, label='Cable 6')
plot(x, var7, label='Cable 7')
legend()

long0 = []
long1 = []
long2 = []
long3 = []
long4 = []
long5 = []
long6 = []
long7 = []

for i in range(n):
    long0.append(longueurCable[i][0])
    long1.append(longueurCable[i][1])
    long2.append(longueurCable[i][2])
    long3.append(longueurCable[i][3])
    long4.append(longueurCable[i][4])
    long5.append(longueurCable[i][5])
    long6.append(longueurCable[i][6])
    long7.append(longueurCable[i][7])

subplot(1, 2, 2)

plot(x, long0, label='Cable 0')
plot(x, long1, label='Cable 1')
plot(x, long2, label='Cable 2')
plot(x, long3, label='Cable 3')
plot(x, long4, label='Cable 4')
plot(x, long5, label='Cable 5')
plot(x, long6, label='Cable 6')
plot(x, long7, label='Cable 7')
show()


######################## Troisième partie : Commande du robot ##################


def commande(trajectoire, pas_maximal, dimensions_physiques_mobile, dimensions_physiques_hangar):
    # Les définitions de tous les arguments sont données respectivement dans discretisation_trajectoire, calcul_pas_adapte, reconstruction_coins, commande_longeurs_cables

    # Cette fonction est la fonction de haut niveau dont on se servira pour commander la maquette.
    # Elle prend en argument la trajectoire souhaitée et renvoie la commande à passer aux moteurs.
    # Ces étapes de fonctionnement sont :
    # - 1 : On discrétise la trajectoire donnée en argument.
    # - 2 : On déduit de la trajectoire discrétisée les variations de longueurs des câbles.
    # - 3 : On traduit ces variations de longueur des câbles en commande de rotation angulaire des moteurs.

    # Cette fonction renvoie une liste des commandes des moteurs. Chaque commande moteur sera à son tour un np.array de dimension 8 dont le ième élément sera la commande destinée au ième moteur.
    diametreTambour = 0.009
    _, trajectoireDiscretise = discretisation_trajectoire(trajectoire, pas_maximal)
    longueurCable = commande_longeurs_cables(trajectoireDiscretisee, dimensions_physiques_mobile, dimensions_physiques_hangar)
    nombrePosition = len(longueurCable)
    rotationMoteur = []
    for i in range(nombrePosition):
        rotation = np.arctan(longueurCable[i]/diametreTambour)
        rotationMoteur += [rotation]

    return rotation


origine = np.array([0., 0., 0., 0., 0., 0.])
destination = np.array([0.5, 0., 0., 0, 0, 0])
# n = calcul_pas_adapte(origine, destination, pas_maximal)


######################## Quatrième partie : Initialisation ##################

# L'objectif de cette partie est de faire l'initialisation visuelle de la maquette pour cela on aura un bouton et un numéro du moteur on pourra donc faire tourner manuellement le moteur


def initialisationRotation(numeroMoteur, bouton):
    # cette fonction prend en argument le numéro du moteur qui est un entier et un bouton qui est fait un True/False
    diametreTambour = 0.009
    rotationMoteur = [0 for k in range(8)]
    if bouton:
        rotationMoteur = arctan(0.01/diametreTambour)
    return rotationMoteur
