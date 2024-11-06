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

def calculate_path_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance_matrix[path[i]][path[i + 1]]
    total_distance += distance_matrix[path[-1]][path[0]]  # Return to start
    return total_distance

def generate_neighbors(path):
    neighbors = []
    for i in range(1, len(path) - 1):
        for j in range(i + 1, len(path)):
            neighbor = path[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def recherche_tabou(solution_initiale, taille_tabou, iter_max, matrix):
    nb_iter = 0                                                                
    liste_tabou = deque((), maxlen = taille_tabou)                             
                                                                               
    # variables solutions pour la recherche du voisin optimal non tabou        
    solution_courante = solution_initiale                                      
    meilleure = solution_initiale                                              
    meilleure_globale = solution_initiale                                       
                                                                               
    # variables valeurs pour la recherche du voisin optimal non tabou          
    valeur_meilleure = calculate_path_distance(solution_initiale, matrix)                       
    valeur_meilleure_globale = valeur_meilleure

    while (nb_iter < iter_max):                                                
        valeur_meilleure = float('inf')                                                  
                                                                               
        # on parcourt tous les voisins de la solution courante                 
        for voisin in generate_neighbors(solution_courante):                            
            valeur_voisin = calculate_path_distance(voisin, matrix)                             
                                                                               
            # MaJ meilleure solution non taboue trouvée                        
            if valeur_voisin < valeur_meilleure and voisin not in liste_tabou: 
                valeur_meilleure = valeur_voisin                               
                meilleure = voisin                                             
                                                                               
        # on met à jour la meilleure solution rencontrée depuis le début       
        if valeur_meilleure < valeur_meilleure_globale:                        
            meilleure_globale = meilleure                                      
            valeur_meilleure_globale = valeur_meilleure                        
            nb_iter = 0                                                        
        else:                                                                  
            nb_iter += 1                                                       
                                                                               
        # on passe au meilleur voisin non tabou trouvé                         
        solution_courante = meilleure                                          
                                                                               
        # on met à jour la liste tabou                                         
        liste_tabou.append(solution_courante)                                  
        
        print(f"Iteration {nb_iter}:")
        # print(f"  Current solution: {solution_courante}")
        print(f"  Current value: {calculate_path_distance(solution_courante, matrix)}")
        # print(f"  Best global solution: {meilleure_globale}")
        print(f"  Best global value: {valeur_meilleure_globale}")
                                                                               
    return meilleure_globale     


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

total_distance = calculate_path_distance(path, distance_matrix)
print(f"total_distance : {total_distance}")

neighbors = generate_neighbors(path)
print(f"neighbors : {neighbors}")


# Initialisation des paramètres
taille_tabou = 10
iter_max = 30
solution_initiale = path
tabou = recherche_tabou(solution_initiale, taille_tabou, iter_max, distance_matrix)
print(f"tabou : {tabou}")
