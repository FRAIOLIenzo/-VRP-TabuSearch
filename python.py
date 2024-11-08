import random
import math
from collections import deque
import matplotlib.pyplot as plt
import time
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value
import statistics
from tqdm import tqdm
from itertools import combinations

#---------------------------------------------------------------Fonctions----------------------------------------------------------------
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
    
    courantes = deque(()) #SOLUTION
    meilleures_courantes = deque(()) #SOLUTION
    # print("nb_voisin : ", len(generate_neighbors(solution_courante))) 
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

def multi_start(nb_villes, solution_initiale, distance_matrix, nb_test):
    taille_tabou = 30
    iter_max = 50

    # multi-start de n itérations
    val_max = float('inf')
    sol_max = None

    sac = solution_initiale
    solutions = []
    best_solutions = []

    for _ in tqdm(range(nb_test)):
        sol_courante, _, _ = recherche_tabou(sac, taille_tabou, iter_max, distance_matrix)
        val_courante = calculate_path_distance(sol_courante, distance_matrix)
        
        solutions.append(val_courante)
        
        if val_courante < val_max:
            val_max = val_courante
            sol_max = sol_courante
        
        best_solutions.append(val_max)
        sac = generate_path(nb_villes, 0)

    return sol_max, val_max, nb_test, solutions, best_solutions

def solve_vrp_with_pulp(distance_matrix):
    num_cities = len(distance_matrix)

    # Create a PuLP problem instance for minimization
    prob = LpProblem("VRP", LpMinimize)

    # Binary variables: x[i][j] == 1 if path i -> j is chosen
    x = LpVariable.dicts("x", ((i, j) for i in range(num_cities) for j in range(num_cities)), cat="Binary")

    # Additional variables to prevent subtours (MTZ formulation)
    u = LpVariable.dicts("u", (i for i in range(num_cities)), lowBound=0, cat="Continuous")

    # Objective: Minimize the total distance
    prob += lpSum(distance_matrix[i][j] * x[i, j] for i in range(num_cities) for j in range(num_cities))

    # Constraints
    # 1. Each city must be entered exactly once
    for j in range(num_cities):
        prob += lpSum(x[i, j] for i in range(num_cities) if i != j) == 1

    # 2. Each city must be left exactly once
    for i in range(num_cities):
        prob += lpSum(x[i, j] for j in range(num_cities) if i != j) == 1

    # 3. Subtour elimination constraints (MTZ formulation)
    for i in range(1, num_cities):
        for j in range(1, num_cities):
            if i != j:
                prob += u[i] - u[j] + num_cities * x[i, j] <= num_cities - 1

    # Solve the problem
    prob.solve()

    # Retrieve the optimal path
    path = []
    if LpStatus[prob.status] == "Optimal":
        # Find the path by tracing x[i][j] == 1
        start = 0
        visited = set([start])
        path.append(start)
        
        while len(visited) < num_cities:
            for j in range(num_cities):
                if value(x[start, j]) == 1:
                    path.append(j)
                    visited.add(j)
                    start = j
                    break
        # Return to starting point to complete the cycle
        path.append(0)
        
        # Total distance
        total_distance = value(prob.objective)
        return path, total_distance
    else:
        return None, None


#---------------------------------------------------------------Plotting----------------------------------------------------------------
def plot_tabu_search_path(coordinates, tabou, tabou_distance, subplot_position):
    plt.subplot(*subplot_position)
    plt.scatter(*zip(*coordinates.values()), c='blue', label="Cities")
    plt.scatter(*coordinates[tabou[0]], c='green', label="Start City")
    for i in range(len(tabou) - 1):
        city1 = coordinates[tabou[i]]
        city2 = coordinates[tabou[i + 1]]
        plt.plot([city1[0], city2[0]], [city1[1], city2[1]], 'r-')
    plt.title(f"Tabu Search Path: {tabou_distance}")
def plot_solution_evolution(courants, meilleurs_courants, subplot_position):
    plt.subplot(*subplot_position)
    plt.plot(range(len(courants)), courants, label='Current Solution', color='blue')
    plt.plot(range(len(meilleurs_courants)), meilleurs_courants, label='Best Solution', color='orange')
    plt.title("Solution Evolution")
    plt.xlabel("Iteration")
    plt.ylabel("Solution Value")
    plt.legend()
def plot_multi_start_best_solution(coordinates, sol_max, val_max, nb_test, subplot_position):
    plt.subplot(*subplot_position)
    plt.scatter(*zip(*coordinates.values()), c='blue', label="Cities")
    plt.scatter(*coordinates[sol_max[0]], c='green', label="Start City")
    for i in range(len(sol_max) - 1):
        city1 = coordinates[sol_max[i]]
        city2 = coordinates[sol_max[i + 1]]
        plt.plot([city1[0], city2[0]], [city1[1], city2[1]], 'r-')
    plt.title(f"Multi-start Best Solution: {val_max}, after {nb_test} attempts")
def plot_solution_statistics(solutions, best_solutions, subplot_position):
    plt.subplot(*subplot_position)
    plt.plot(range(len(solutions)), solutions, label='Current Solutions', color='blue')
    plt.plot(range(len(best_solutions)), best_solutions, label='Best Solutions', color='orange')
    plt.title("Solution Evolution Over Multiple Starts")
    plt.xlabel("Iteration")
    plt.ylabel("Solution Value")
    plt.legend()
def plot_exact_solution_pulp(coordinates, pulp_path, pulp_distance, tabou_distance, subplot_position):
    plt.subplot(*subplot_position)
    plt.scatter(*zip(*coordinates.values()), c='blue', label="Cities")
    plt.scatter(*coordinates[pulp_path[0]], c='green', label="Start City")
    for i in range(len(pulp_path) - 1):
        city1 = coordinates[pulp_path[i]]
        city2 = coordinates[pulp_path[i + 1]]
        plt.plot([city1[0], city2[0]], [city1[1], city2[1]], 'r-')
    ratio = tabou_distance / pulp_distance if pulp_distance != 0 else float('inf')
    plt.title(f"Exact Solution PuLP: {pulp_distance}, Ratio: {ratio:.2f}")

def plot_vrp_solutions( tabou, tabou_distance, courants, meilleurs_courants, nb_villes):
    plt.figure(figsize=(15, 10))
    plot_tabu_search_path(coordinates, tabou, tabou_distance, (2, 2, 1))
    plot_solution_evolution(courants, meilleurs_courants, (2, 2, 2))

    # Add overall title
    plt.suptitle(f"VRP Solutions for {nb_villes} cities")
    plt.tight_layout()
    plt.show()
def plot_multi_vrp_solutions(coordinates, tabou, tabou_distance, courants, meilleurs_courants, sol_max, val_max, nb_villes, nb_test, solutions, best_solutions):
    plt.figure(figsize=(15, 10))
    plot_tabu_search_path(coordinates, tabou, tabou_distance, (2, 2, 1))
    plot_solution_evolution(courants, meilleurs_courants, (2, 2, 2))
    plot_multi_start_best_solution(coordinates, sol_max, val_max, nb_test, (2, 2, 3))
    plot_solution_statistics(solutions, best_solutions, (2, 2, 4))

    # Add overall title
    plt.suptitle(f"VRP Solutions for {nb_villes} cities")
    plt.tight_layout()
    plt.show()
def plot_all_vrp_solutions(coordinates, tabou, tabou_distance, courants, meilleurs_courants, sol_max, val_max, pulp_path, pulp_distance, nb_villes, nb_test):
    plt.figure(figsize=(15, 10))

    plot_tabu_search_path(coordinates, tabou, tabou_distance, (2, 2, 1))
    plot_solution_evolution(courants, meilleurs_courants, (2, 2, 2))
    plot_exact_solution_pulp(coordinates, pulp_path, pulp_distance, tabou_distance, (2, 2, 3))
    plot_multi_start_best_solution(coordinates, sol_max, val_max, nb_test, (2, 2, 4))

    # Add overall title
    plt.suptitle(f"VRP Solutions for {nb_villes} cities")
    plt.tight_layout()
    plt.show()

#---------------------------------------------------------------Stat----------------------------------------------------------------
def test_tabou_search_impact(tabou_min, tabou_max, nb_villes, nb_test, iter_max):
    # Initialisation des résultats
    moyennes = []
    deviations = []

    # Fixer la graine pour la reproductibilité
    random.seed(9)

    # Génération aléatoire de l'instance
    coordinates = generate_coordinates(nb_villes)
    distances_dict = calculate_distances(coordinates)
    distance_matrix = distances_to_matrix(distances_dict, nb_villes)

    # Boucle sur la taille de la liste tabou
    for taille_tabou in tqdm(range(tabou_min, tabou_max)):
        distances = deque()
        
        for _ in range(nb_test):
            # Générer un chemin initial
            path = generate_path(nb_villes, 0)
            
            # Appliquer la recherche tabou
            solution, _, _ = recherche_tabou(path, taille_tabou, iter_max, distance_matrix)
            
            # Calculer la distance du chemin solution
            val = calculate_path_distance(solution, distance_matrix)
            distances.append(val)

        # Calcul des statistiques pour la taille de liste tabou courante
        moyennes.append(statistics.mean(distances))
        deviations.append(statistics.stdev(distances))

    # Affichage des résultats
    plt.plot(range(tabou_min, tabou_max), moyennes, label="Moyenne des distances")
    
    # Affichage de la bande d'écart-type
    plt.fill_between(range(tabou_min, tabou_max),
                     [m - d for m, d in zip(moyennes, deviations)],
                     [m + d for m, d in zip(moyennes, deviations)],
                     alpha=0.1, label="Écart-type")
    plt.xlabel("Taille de la liste tabou")
    plt.ylabel("Distance du parcours")
    plt.title("Impact de la taille de la liste tabou sur la qualité des solutions")
    plt.legend()
    plt.show()

    return moyennes, deviations

#---------------------------------------------------------------Main----------------------------------------------------------------
print("Main")
nb_villes = 20

coordinates = generate_coordinates(nb_villes)
distances = calculate_distances(coordinates)
distance_matrix = distances_to_matrix(distances, nb_villes)
random.seed(9)
path = generate_path(nb_villes, 0)
random.seed()
start = time.process_time()

# Initialisation des paramètres
taille_tabou = 140
iter_max = 50 
solution_initiale = path
tabou, courants, meilleurs_courants = recherche_tabou(solution_initiale, taille_tabou, iter_max, distance_matrix)
tabou_distance = calculate_path_distance(tabou, distance_matrix)
stop = time.process_time()
print("calculé en ", stop-start, 's')
print("Distance : ", tabou_distance)
# plot_vrp_solutions(tabou, tabou_distance, courants, meilleurs_courants, nb_villes)

# Run multi start
nb_test = 30
sol_max, val_max, nb_test, solutions, best_solutions = multi_start(nb_villes, solution_initiale, distance_matrix, nb_test)
plot_multi_vrp_solutions(coordinates, tabou, tabou_distance, courants, meilleurs_courants, sol_max, val_max, nb_villes, nb_test, solutions, best_solutions)

print("solutions : ", solutions)
print("best_solutions : ", best_solutions)



# # Run the exact solver
# pulp_path, pulp_distance = solve_vrp_with_pulp(distance_matrix)
# plot_all_vrp_solutions(coordinates, tabou, tabou_distance, courants, meilleurs_courants, sol_max, val_max, pulp_path, pulp_distance, nb_villes, nb_test)

#Run Test Tabou Search Impact
# tabou_min = 1
# tabou_max = 200
# nb_villes = 20
# nb_test = 100
# iter_max = 20
# test_tabou_search_impact(tabou_min, tabou_max, nb_villes, nb_test, iter_max)