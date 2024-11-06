import numpy as np
from collections import deque

def tabu_search_tsp(distances, max_iterations=100, tabu_list_size=10):
    """
    Résolution du problème du voyageur de commerce (TSP) par recherche tabou.

    Paramètres :
    distances (numpy.ndarray) : Matrice des distances entre les villes
    max_iterations (int) : Nombre maximum d'itérations
    tabu_list_size (int) : Taille de la liste tabou

    Retourne :
    list : La meilleure tournée trouvée
    """
    n = len(distances)
    current_tour = list(range(n))
    np.random.shuffle(current_tour)
    best_tour = current_tour[:]
    best_distance = calculate_distance(distances, current_tour)

    tabu_list = deque(maxlen=tabu_list_size)

    for _ in range(max_iterations):
        neighbors = generate_neighbors(current_tour)
        best_neighbor = None
        best_neighbor_distance = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_distance = calculate_distance(distances, neighbor)
                if neighbor_distance < best_neighbor_distance:
                    best_neighbor = neighbor
                    best_neighbor_distance = neighbor_distance

        if best_neighbor is None:
            break

        tabu_list.append(current_tour)
        current_tour = best_neighbor[:]

        if best_neighbor_distance < best_distance:
            best_tour = best_neighbor[:]
            best_distance = best_neighbor_distance

    return best_tour

def generate_neighbors(tour):
    """
    Génère les voisins d'une tournée en échangeant deux villes.
    """
    neighbors = []
    for i in range(len(tour)):
        for j in range(i + 1, len(tour)):
            neighbor = tour[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def calculate_distance(distances, tour):
    """
    Calcule la distance totale d'une tournée.
    """
    total_distance = 0
    for i in range(len(tour)):
        total_distance += distances[tour[i], tour[(i + 1) % len(tour)]]
    return total_distance

# Distances between major French cities: Paris, Lyon, Marseille, Bordeaux, Toulouse, Nantes, Strasbourg, Lille, Nice, Rennes
distances = np.array([
    # Paris, Lyon, Marseille, Bordeaux, Toulouse, Nantes, Strasbourg, Lille, Nice, Rennes
    [0, 463, 773, 585, 678, 380, 488, 225, 932, 351],  # Paris
    [463, 0, 315, 556, 538, 628, 492, 688, 472, 727],  # Lyon
    [773, 315, 0, 506, 407, 940, 800, 1001, 158, 1048],  # Marseille
    [585, 556, 506, 0, 245, 338, 939, 792, 802, 443],  # Bordeaux
    [678, 538, 407, 245, 0, 580, 987, 919, 804, 675],  # Toulouse
    [380, 628, 940, 338, 580, 0, 857, 584, 1088, 107],  # Nantes
    [488, 492, 800, 939, 987, 857, 0, 524, 959, 800],  # Strasbourg
    [225, 688, 1001, 792, 919, 584, 524, 0, 1160, 575],  # Lille
    [932, 472, 158, 802, 804, 1088, 959, 1160, 0, 1196],  # Nice
    [351, 727, 1048, 443, 675, 107, 800, 575, 1196, 0]   # Rennes
])

best_tour = tabu_search_tsp(distances)
total_distance = calculate_distance(distances, best_tour)
print(f"Distance totale du meilleur tour: {total_distance}")
print(best_tour)