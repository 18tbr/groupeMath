# Ce squelette de code n'est qu'une proposition de structure pour votre code de commande du robot, si vous vouhaitez vous en écarter ou l'améliorer sentez vous libre.

# On suppose que l'on a une série de points en entrée, on s'occupera de ce détail plus tard.

import numpy as np  # Le code qui gère les rotations, etc... A besoin de numpy donc pour éviter les problèmes le plus simple est que tout le monde utilise numpy.
import math

################ Première partie : Discrétisation de la trajectoire ############

# La première chose est de découper cette trajectoire en une série de petits pas à faire. La démarche que vous avez proposée me semble être la bonne, don on va la suivre.

pas_translation_x = 0.1
pas_translation_y = 0.1
pas_translation_z = 0.1
pas_rotation_alpha = 1 # angle en degré
pas_rotation_beta = 1
pas_rotation_gama = 1
pas_maximal = np.array([pas_translation_x, pas_translation_y, pas_translation_z, pas_rotation_alpha, pas_rotation_beta, pas_rotation_gama])


def calcul_pas_adapte(origine, destination, pas_maximal):
    diff = np.zeros(6)
    nombre_pas = np.zeros(6)
    for i in range(6):
        diff[i] = destination[i] - origine[i]
        nombre_pas[i] = diff[i] / pas_maximal[i]
    nombre_pas_max = np.amax(nombre_pas)
    return nombre_pas_max
            
    # origine est un vecteur à 6 dimensions (3 positions et 3 angles), idem pour la destination. Leur type est np.array.
    # Notez que pas maximal est aussi un vecteur à 6 dimensions, qui contient le maximal que l'on s'autorise dans chaque dimension.

    # Pour calculer le pas adapté vous pouvez réutiliser ce que vous avez écrit, à savoir :
    # - 1 : On calcule le nombre de pas minimal que l'on devra faire pour aller de la source à la destination (attention, il faut atteindre la destination selon toutes les dimensions, donc c'est la dernière dimension atteinte qui dicte le nombre de pas);
    # - 2 : On calcul le pas dont on a besoin pour aller de l'origine à la destination en faisant le nombre minimal de pas trouvé précédement mais en s'asurant que ces pas soient de longueur constante.

    # On renvoie enfin le nombre de pas à faire (un entier) et la longueur de ces pas (un flottant).

#Test
origine = np.array([0,0,0,0,0,0])
destination = np.array([0.5,0,0,0,0,0])
n = calcul_pas_adapte(origine, destination, pas_maximal)

#Definir la trajectoire_souhaitee
trajectoire_souhaitee = np.array([origine], dtype = float)
trajectoire_souhaitee = np.insert(trajectoire_souhaitee, 1, destination, 0)


def discretisation_trajectoire(nombre_pas, trajectoire_souhaitee, pas_maximal):
    
    variation = np.array([[0,0,0,0,0,0]])
    
    dx = (trajectoire_souhaitee[1][0] - trajectoire_souhaitee[0][0])/nombre_pas
    dy = (trajectoire_souhaitee[1][1] - trajectoire_souhaitee[0][1])/nombre_pas
    dz = (trajectoire_souhaitee[1][2] - trajectoire_souhaitee[0][2])/nombre_pas
    dalpha = (trajectoire_souhaitee[1][3] - trajectoire_souhaitee[0][3])/nombre_pas
    dbeta = (trajectoire_souhaitee[1][4] - trajectoire_souhaitee[0][4])/nombre_pas
    dgama = (trajectoire_souhaitee[1][5] - trajectoire_souhaitee[0][5])/nombre_pas
    
    for i in range (1, math.ceil(nombre_pas)): 
        
        x = trajectoire_souhaitee[0][0] + i * dx
        y = trajectoire_souhaitee[0][1] + i * dy
        z = trajectoire_souhaitee[0][2] + i * dz
        alpha = trajectoire_souhaitee[0][3] + i * dalpha
        beta = trajectoire_souhaitee[0][4] + i * dbeta
        gama = trajectoire_souhaitee[0][5] + i * dgama
        
        trajectoire_souhaitee = np.insert(trajectoire_souhaitee, i, [x,y,z,alpha,beta,gama], 0)
        print([[dx,dy,dz,dalpha,dbeta,dgama]])
        variation = np.insert(variation, i, [dx,dy,dz,dalpha,dbeta,dgama],0)
        
    return [trajectoire_souhaitee, variation]
    
    # On passe en passe en argument la trajectoire souhaitée, qui est une liste de tableaux numpy, chaque tableau numpy ayant 6 dimensions, 3 positions + 3 angles.
    # pas_maximal est défini comme dans calcul_pas_adapte

    # Cette fonction discrétise la trajectoire souhaitée en divisant les parties trop grandes en pas de longueurs constantes par morceaux toujours plus petits que pas_maximal

    # Cette fonction renvoie une liste non pas des points par lesquels il faut passer (on n'en a pas besoin, mais si vous le souhaitez vous pouvez aussi renvoyer cette liste pour tracer des courbes), mais plutôt des déplacements infinitésimaux qu'il faut pour passer d'un point à un autre.
    # Chacun de ces déplacements infintésimaux est un np.array de 6 dimensions, 3 déplacements en position et 3 déplacements angulaires.

#Test
[trj, var] = discretisation_trajectoire(n, trajectoire_souhaitee, pas_maximal)
# la trajectoire a l'air de marcher, mais je comprends pas pourquoi la vararion donne tjrs 0




# np.array, dans une gande liste


##################### Deuxième partie : Longueur des câbles ####################

# On arrive dans la partie du code qui convertit les déplacements infintésimaux du mobile en variations de longueurs des câbles.
# Pour cette partie on va suivre votre idée d'utiliser des matrices de rotation qui devrait effectivement simplifier votre code.

def reconstruction_coins(position_mobile, dimensions_physiques_mobile):
    # L'argument position_mobile est un np.array à 6 dimensions, 3 positions + 3 angles, représentant la position actuelle du centre du mobile et son orientation.
    # dimensions_physiques_mobile est un np.array de 3 dimensions représentant longeur, largeur et hauteur du mobile.

    # Pour l'écriture de cette fonction on va reprendre en grande partie ce que vous avez déjà fait :
    # - 1 : On crée un image du mobile aux dimensions mais aligné avec la base du hangar et collé contre l'origine.
    # - 2 : On oriente le mobile pour qu'il soit aligné avec l'orientation donnée par base_mobile (en utilisant des matrices de rotation pour arriver à l'orientation souhaitée depuis l'orientation d'origine du hangar).
    # - 3 : On déplace le mobile pour que son centre se retrouve à la position donnée par position_mobile.

    # Cette fonction renverra un liste de 8 éléments des positions des huits coins dans l'espace. La position d'un coin sera un np.array de dimension 3 (x, y et z)
    pass

def calcul_longueurs_cables(positions_coins_mobile, positions_coins_hangar):
    # L'argument positions_coins_mobile est une liste (de taille 8) des coins du mobile, chaque coin étant donnée sous la forme d'un np.array de dimension 3 (x, y et z) dans l'ordre de la numérotation donnée sur votre schéma.
    # De même positions_coins_hangar est une liste (de taille 8) des positions des coins du hangar, chaque position étant un np.array de dimension 3 et l'ordre étant celui donnée sur votre schéma.

    # Pour l'écriture de cette fonction on peut complémtement reprendre ce que vous avez fait, notamment le fait d'utiliser une liste de correspondances est une bonne idée pour avoir un code plus compact.

    # Cette fonction renverra un np.array de 8 éléments, le ième élément correspondant à la longueur du ième câble.
    pass

def construction_rectangle(dimensions, centre):
    # dimensions contient les dimensions physiques du rectangle que l'on souhaite construire. Il s'agit d'un np.array de dimension 3 (x, y et z).
    # centre est un booleen qui indique si l'on doit placer le centre du rectangle sur l'origine ou plutôt le coin A6. True signifie que le centre doit être placé à l'origine (pour le mobile) et False signifie que le coin A6 doit être placé à l'origine.

    # Cette fonction annexe mais utile est celle que vous avez défini dans votre code comme coinHangar.
    # Je pense qu'elle va effectivement vous permettre d'avoir un code plus simple à lire.

    # Cette fonction renvoie une liste de taille 8 des coordonnées des points du rectangle collé contre l'origine et orienté comme le hangar. Chaque coordonnée de coin du rectangle sera un np.array de dimension 3 (x, y et z)
    pass

def rotation(rho, theta, phi):
    # rho, theta et phi sont des déplacements angulaires du mobile autour des trois vecteurs de la base du hangar.

    # Je vous propose aussi cette fonction annexe qui pourrait vous être utile. Ele prend en argument trois angles de rotation et renvoie la matrice prosuit des trois rotations obtenues (i.e. Rx*Ry*Rz).
    # Multiplier une vecteur par la matrice obtenue permettra de lui faire subir les trois rotations.

    # Cette fontion renvoie un np.array de dimensions 3*3 défini comme le produit des trois matrices de rotations données respectivement par les angles rho, theta, phi.
    pass

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
    pass


######################## Troisième partie : Commande du robot ##################

def commande(trajectoire_souhaitee, pas_maximal, dimensions_physiques_mobile, dimensions_physiques_hangar):
    # Les définitions de tous les arguments sont données respectivement dans discretisation_trajectoire, calcul_pas_adapte, reconstruction_coins, commande_longeurs_cables

    # Cette fonction est la fonction de haut niveau dont on se servira pour commander la maquette.
    # Elle prend en argument la trajectoire souhaitée et renvoie la commande à passer aux moteurs.
    # Ces étapes de fonctionnement sont :
    # - 1 : On discrétise la trajectoire donnée en argument.
    # - 2 : On déduit de la trajectoire discrétisée les variations de longueurs des câbles.
    # - 3 : On traduit ces variations de longueur des câbles en commande de rotation angulaire des moteurs.

    # Cette fonction renvoie une liste des commandes des moteurs. Chaque commande moteur sera à son tour un np.array de dimension 8 dont le ième élément sera la commande destinée au ième moteur.
    pass
