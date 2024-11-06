import random


def generate_coordinates(nb_villes, x_max=100, y_max=100):
    coordinates = []
    for _ in range(nb_villes):
        x = random.randint(1, x_max)
        y = random.randint(1, y_max)
        coordinates.append((x, y))
    return coordinates



nb_villes = 10
coordinates = generate_coordinates(nb_villes)
print(coordinates)





# DONE : faire valeur aléatoire pour représenter les coordonées des villes pour VRP
# TODO : faire algo pour trouver distance entre toutes les villes 
# TODO : enlever valeur des objets 
# TODO : enlever capacité du sac car on ne l'utilise pas dans le TSP
# TODO : passer par toutes les villes avec même départ
# TODO : changer les voisins aléatoirement pour avoir une distance plus courte 
# TODO : faire les stat descriptive sur cette algo 