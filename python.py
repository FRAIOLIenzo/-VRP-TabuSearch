import random
import math
from collections import deque
from functools import lru_cache

# DONE : faire valeur aléatoire pour représenter les coordonées des villes pour VRP
# DONE : faire algo pour trouver distance entre toutes les villes 
# TODO : faire path commun pour VRP
# TODO : passer par toutes les villes avec même départ
# TODO : changer les voisins aléatoirement pour avoir une distance plus courte 
# TODO : faire les stat descriptive sur cette algo 

random.seed(10)
def generate_coordinates(nb_villes, x_max=100, y_max=100):
    coordinates = {}
    for i in range(nb_villes):
        x = random.randint(1, x_max)
        y = random.randint(1, y_max)
        coordinates[i] = (x, y)
    return coordinates

def calculate_distances(coordinates):
    distances = {}
    for i, (x1, y1) in coordinates.items():
        for j, (x2, y2) in coordinates.items():
            if i != j:
                distance = round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                distances[(i, j)] = distance
    return distances

def distances_to_matrix(distances, nb_villes):
    matrix = [[0] * nb_villes for _ in range(nb_villes)]
    for (i, j), distance in distances.items():
        matrix[i][j] = distance
    return matrix

def generate_path(nb_villes, start_city):
    path = list(range(nb_villes))
    path.remove(start_city)
    path.insert(0, start_city)
    return path




# Main
nb_villes = 10

coordinates = generate_coordinates(nb_villes)
print(f"coordinates : {coordinates}")

distances = calculate_distances(coordinates)
print(f"distances : {distances}")
print("--------------------")
distance_matrix = distances_to_matrix(distances, nb_villes)
for row in distance_matrix:
    print(" ".join(f"{dist:3}" for dist in row))
print("--------------------")

path = generate_path(nb_villes, 0)
print(f"path : {path}")