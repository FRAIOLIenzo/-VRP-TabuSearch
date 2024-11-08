import random
import math
from collections import deque
import matplotlib.pyplot as plt
import time
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value
import statistics
from tqdm import tqdm



def generate_coordinates(nb_villes, x_max=100, y_max=100, min_distance=5):
    random.seed(9)
    coordinates = {}
    while len(coordinates) < nb_villes:
        x = random.randint(1, x_max)
        y = random.randint(1, y_max)
        if all(math.sqrt((x - cx) ** 2 + (y - cy) ** 2) >= min_distance for cx, cy in coordinates.values()):
            coordinates[len(coordinates)] = (x, y)
    random.seed()
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
    random.shuffle(path)
    path.insert(0, start_city)
    path.append(start_city)  
    return path

def calculate_path_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance_matrix[path[i]][path[i + 1]]
    total_distance += distance_matrix[path[-1]][path[0]] 
    return total_distance

def generate_neighbors(path):
    neighbors = []
    from itertools import combinations
    for i, j in combinations(range(1, len(path) - 1), 2):
            path[i], path[j] = path[j], path[i]
            neighbors.append(path[:])
            path[i], path[j] = path[j], path[i]
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
    
    # liste des solutions courantes et des meilleures trouvées, pour afficher la trajectoire
    # l'élément à la ième position correspond à l'itération i
    courantes = deque(()) #SOLUTION
    meilleures_courantes = deque(()) #SOLUTION
    
    # print(f"Initial solution: {solution_initiale}")
    # print(calculate_path_distance(solution_initiale, matrix))

    while (nb_iter < iter_max):                                                
        valeur_meilleure = float('inf')                                                 
                                                                               
        # on parcourt tous les voisins de la solution courante                 
        for voisin in generate_neighbors(solution_courante):  
            # print("nb_voisin : ", len(generate_neighbors(solution_courante)))                          
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

        courantes.append(calculate_path_distance(solution_courante, matrix)) 
        meilleures_courantes.append(valeur_meilleure_globale) 

                                                             
                                                                               
        # on passe au meilleur voisin non tabou trouvé                         
        solution_courante = meilleure                                          
                                                                               
        # on met à jour la liste tabou                                         
        liste_tabou.append(solution_courante)                                  
        
        # print(f"Iteration {nb_iter}:")
        # print(f"  Current solution: {solution_courante}")
        # print(f"  Current value: {calculate_path_distance(solution_courante, matrix)}")
        # print(f"  Best global solution: {meilleure_globale}")
        # print(f"  Best global value: {valeur_meilleure_globale}")
                                                                               
    return meilleure_globale, courantes, meilleures_courantes     



# Main -----------------------------------------------------------------------------------
print("Main")
nb_villes = 100

coordinates = generate_coordinates(nb_villes)

# Plot the cities
# plt.scatter(*zip(*coordinates.values()))
# plt.title("City Coordinates")
# plt.xlabel("X Coordinate")
# plt.ylabel("Y Coordinate")
# plt.show()

distances = calculate_distances(coordinates)

distance_matrix = distances_to_matrix(distances, nb_villes)

random.seed(9)
path = generate_path(nb_villes, 0)
random.seed()

start = time.process_time()
# Initialisation des paramètres
taille_tabou = 10
iter_max = 20 
solution_initiale = path
tabou, courants, meilleurs_courants = recherche_tabou(solution_initiale, taille_tabou, iter_max, distance_matrix)
tabou_distance = calculate_path_distance(tabou, distance_matrix)
stop = time.process_time()
print(f"tabou : {tabou}")



# Plot the cities and the path found by the Tabu Search
plt.scatter(*zip(*coordinates.values()), c='blue')
plt.scatter(*coordinates[tabou[0]], c='green')  # Make the start city green
for i in range(len(tabou) - 1):
    city1 = coordinates[tabou[i]]
    city2 = coordinates[tabou[i + 1]]
    plt.plot([city1[0], city2[0]], [city1[1], city2[1]], 'r-')
plt.title(f"Path found by Tabu Search: {tabou_distance} for {nb_villes} cities")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.show()
print(f"tabou_distance : {tabou_distance}")
print("calculé en ", stop-start, 's')

# Plot the evolution of the current solution and the best solution found
plt.title(f"Best Tabu Value: {tabou_distance} for {nb_villes} cities")
plt.xlabel("nb itérations", fontsize=16)
plt.ylabel("valeur", fontsize=16)
plt.plot(range(len(courants)), courants, label='Solution courante')
plt.plot(range(len(courants)), meilleurs_courants, label='Meilleure solution')
plt.legend()

plt.show()

# 264 for 10
#Pulp 190
# 1367 for 100 1317
#Pulp 566
# 2483 for 200 !! 52 secondes !!

#---------------------------------------------------PULP

# def borne_inferieure():
#     villes = range(nb_villes)

#     # variables
#     x = LpVariable.dicts('route', ((i,j) for i in villes for j in villes if i!=j), 0, 1)
    
#     # probleme
#     prob = LpProblem("tsp_relaxation", LpMinimize)

#     # fonction objective
#     cost = lpSum(distance_matrix[i][j] * x[i,j] for i in villes for j in villes if i!=j)
#     prob += cost

#     # contraintes
#     for i in villes:
#         prob += lpSum(x[i,j] for j in villes if i!=j) == 1  # chaque ville doit être quittée une fois
#         prob += lpSum(x[j,i] for j in villes if i!=j) == 1  # chaque ville doit être visitée une fois

#     # contrainte additionnelle: revenir à la ville de départ
#     prob += lpSum(x[0,j] for j in villes if j != 0) == 1  # partir de la ville de départ
#     prob += lpSum(x[j,0] for j in villes if j != 0) == 1  # revenir à la ville de départ

#     prob.solve()
#     return value(prob.objective) if (LpStatus[prob.status] == "Optimal") else None

# borne = borne_inferieure()
# if borne is not None:
#     print("borne inférieure : ", borne)
# print("valeur de la solution tabou:", str(tabou_distance))

#-------------------------------------------------------------------MULTI-START

# taille_tabou = 60
# iter_max = 10

# # multi-start de 500 itérations
# val_max = float('inf')
# sol_max = None

# sac = solution_initiale
# for _ in range(10):

#     print("sac = " + str(sac))
#     print("valeur initiale = " + str(calculate_path_distance(sac, distance_matrix)))

#     sol_courante, _, _ = recherche_tabou(sac, taille_tabou, iter_max, distance_matrix)
#     val_courante = calculate_path_distance(sol_courante, distance_matrix)
#     print("valeur courante = " + str(val_courante))
    
#     if val_courante < val_max:
#         print("nouveau max = " + str(val_courante))
#         val_max = val_courante
#         sol_max = sol_courante
#     sac = generate_path(nb_villes, 0)

# print("valeur finale = " + str(val_max))

#---------------------------------------------------------------Statistique Liste Tabou


# # paramètres du test
# tabou_min = 1
# tabou_max = 100
# nb_villes = 10

# nb_test = 100
# iter_max = 20

# # pour stocker les résultats
# moyennes = []
# deviations = []

# random.seed(9)


# # génération aléatoire de l'instance 
# coordinates = generate_coordinates(nb_villes)
# distances_dict = calculate_distances(coordinates)
# distance_matrix = distances_to_matrix(distances_dict, nb_villes)

# # boucle sur la taille de la liste tabou
# for taille_tabou in tqdm(range(tabou_min, tabou_max)):
#     distances = deque(())
#     for _ in range(nb_test):

#         path = generate_path(nb_villes, 0)
#         solution, _, _ = recherche_tabou(path, taille_tabou, iter_max, distance_matrix)
#         val = calculate_path_distance(solution, distance_matrix)
#         distances.append(val)
        
                                                            
#     moyennes.append(statistics.mean(distances))
#     deviations.append(statistics.stdev(distances))

# # affichage de la courbe de moyenne
# plt.plot(range(tabou_min, tabou_max), moyennes)

# # affichage de la bande d'écart-type
# plt.fill_between(range(tabou_min, tabou_max),
#                  [m - d for m, d in zip(moyennes, deviations)],
#                  [m + d for m, d in zip(moyennes, deviations)],
#                  alpha=.1)
# plt.xlabel("taille de la liste tabou")
# plt.ylabel("distance du parcours")
# plt.title("Impact de la taille de la liste tabou sur la qualité des solutions")
# plt.show()

#---------------------------------------------------------------Statistique iter_max

# # paramètres du test
# iter_min = 1
# iter_max = 100
# nb_villes = 10

# nb_test = 100
# taille_tabou = 20

# # pour stocker les résultats
# moyennes = []
# deviations = []

# random.seed(9)

# # génération aléatoire de l'instance 
# coordinates = generate_coordinates(nb_villes)
# distances_dict = calculate_distances(coordinates)
# distance_matrix = distances_to_matrix(distances_dict, nb_villes)

# # boucle sur le nombre d'itérations max
# for iterations in tqdm(range(iter_min, iter_max)):
#     distances = deque(())
#     for _ in range(nb_test):
#         path = generate_path(nb_villes, 0)
#         solution, _, _ = recherche_tabou(path, taille_tabou, iterations, distance_matrix)
#         val = calculate_path_distance(solution, distance_matrix)
#         distances.append(val)
                                                            
#     moyennes.append(statistics.mean(distances))
#     deviations.append(statistics.stdev(distances))

# # affichage de la courbe de moyenne
# plt.plot(range(iter_min, iter_max), moyennes)

# # affichage de la bande d'écart-type
# plt.fill_between(range(iter_min, iter_max),
#                  [m - d for m, d in zip(moyennes, deviations)],
#                  [m + d for m, d in zip(moyennes, deviations)],
#                  alpha=.1)
# plt.xlabel("nombre d'itérations maximum")
# plt.ylabel("distance du parcours") 
# plt.title("Impact du nombre d'itérations sur la qualité des solutions")
# plt.show()