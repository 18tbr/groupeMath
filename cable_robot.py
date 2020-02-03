import numpy as np

def auto(array, temps):
    print("auto")
    for i in range(np.shape(array)[0]):
        print(i, array[i], temps)

def manual(vecteur, temps):
    print("manual")
    print(vecteur, temps)

def halt():
    print("Interrupting")
