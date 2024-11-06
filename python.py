import random
import math

# DONE : faire valeur aléatoire pour représenter les coordonées des villes pour VRP
# DONE : faire algo pour trouver distance entre toutes les villes 
# TODO : enlever valeur des objets 
# TODO : enlever capacité du sac car on ne l'utilise pas dans le TSP
# TODO : passer par toutes les villes avec même départ
# TODO : changer les voisins aléatoirement pour avoir une distance plus courte 
# TODO : faire les stat descriptive sur cette algo 

random.seed(10)

def generate_coordinates(nb_villes, x_max=100, y_max=100):
    coordinates = []
    for _ in range(nb_villes):
        x = random.randint(1, x_max)
        y = random.randint(1, y_max)
        coordinates.append((x, y))
    return coordinates

def calculate_distances(coordinates):
    distances = {}
    for i, (x1, y1) in enumerate(coordinates):
        for j, (x2, y2) in enumerate(coordinates):
            if i != j:
                distance = round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                distances[(i, j)] = distance
    return distances

def distances_to_matrix(distances, nb_villes):
    matrix = [[0] * nb_villes for _ in range(nb_villes)]
    for (i, j), distance in distances.items():
        matrix[i][j] = distance
    return matrix



nb_villes = 10
coordinates = generate_coordinates(nb_villes)
print(f"coordinates : {coordinates}")

distances = calculate_distances(coordinates)
print(f"distances : {distances}")

distance_matrix = distances_to_matrix(distances, nb_villes)
for row in distance_matrix:
    print(" ".join(f"{dist:3}" for dist in row))


