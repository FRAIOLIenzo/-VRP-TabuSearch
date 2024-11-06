from collections import deque
import random
from functools import lru_cache

def random_objets(poids_max, val_max):
    """
    Cette fonction génère des objets de poids et de valeur
    aléatoires (bornés par les valeurs passées en parametre).
    
    Renvoie un tuple de 2 dictionnaires (poids,valeur)
    """
    poids_objets =\
        {i: random.randint(1, poids_max) for i in range(nb_objets)} 
    valeur_objets =\
        {i: random.randint(1, val_max) for i in range(nb_objets)}   
                                                                    
    return poids_objets, valeur_objets                              
                                                      

@lru_cache(maxsize=None)
def poids_contenu(sac):
    """
    Cette fonction renvoie la somme des poids des objets dans le sac
    """
    return sum(poids_objets[i] for i, val in enumerate(sac) if val) 

@lru_cache(maxsize=None)
def valeur_contenu(sac):
    """
    Cette fonction renvoie la somme des valeurs des objets dans le sac
    """
    return sum(valeur_objets[i] for i, val in enumerate(sac) if val) 

@lru_cache(maxsize=None)
def voisinage(sac):
    """
    Génère tous les voisins d'une solution en inversant l'inclusion/exclusion
    de chaque objet dans le sac, tout en respectant la contrainte de capacité.
    """
    voisins = []                                                     
    for k in range(len(sac)):                                        
        voisin = sac[:k] + (not(sac[k]),) + sac[k+1:]                
        if (poids_contenu(voisin) <= capacite):                      
            voisins.append(voisin)                                   
    return voisins                                                   

def recherche_tabou(solution_initiale, taille_tabou, iter_max):
    """
    Algorithme de recherche tabou pour optimiser la valeur des objets dans le sac.
    1. On part d'un élément de notre ensemble de recherche qu'on déclare élément courant
    2. On considère le voisinage de l'element courant et on choisit le  meilleur d'entre
       eux comme nouvel element courant, parmi ceux absents de la liste tabou, et on l'ajoute
       a la liste tabou
    3. On boucle jusqu'a condition de sortie.
    """
    nb_iter = 0                                                                
    liste_tabou = deque((), maxlen = taille_tabou)                             
                                                                               
    # variables solutions pour la recherche du voisin optimal non tabou        
    solution_courante = solution_initiale                                      
    meilleure = solution_initiale                                              
    meilleure_globale = solution_initiale                                       
                                                                               
    # variables valeurs pour la recherche du voisin optimal non tabou          
    valeur_meilleure = valeur_contenu(solution_initiale)                       
    valeur_meilleure_globale = valeur_meilleure                                
    
    print(f"Initial solution: {solution_initiale}")
    print(f"Initial value: {valeur_meilleure}")
                                                                               
    while (nb_iter < iter_max):                                                
        valeur_meilleure = -1                                                  
                                                                               
        # on parcourt tous les voisins de la solution courante                 
        for voisin in voisinage(solution_courante):                            
            valeur_voisin = valeur_contenu(voisin)                             
                                                                               
            # MaJ meilleure solution non taboue trouvée                        
            if valeur_voisin > valeur_meilleure and voisin not in liste_tabou: 
                valeur_meilleure = valeur_voisin                               
                meilleure = voisin                                             
                                                                               
        # on met à jour la meilleure solution rencontrée depuis le début       
        if valeur_meilleure > valeur_meilleure_globale:                        
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
        print(f"  Current solution: {solution_courante}")
        print(f"  Current value: {valeur_contenu(solution_courante)}")
        print(f"  Best global solution: {meilleure_globale}")
        print(f"  Best global value: {valeur_meilleure_globale}")
                                                                               
    return meilleure_globale                                                   

# Initialisation des paramètres
nb_objets = 100
capacite = 20
random.seed(a=3)
poids_objets, valeur_objets = random_objets(10, 10)
print("-------------------")
print(random_objets(10, 10))
sac = (False,)*nb_objets

print("tabou de taille 5")
sol = recherche_tabou(sac, taille_tabou=5, iter_max=30)
print("valeur finale = " + str(valeur_contenu(sol)) + ", capacite="+str(poids_contenu(sol)) + "/" + str(capacite))
print([i for i, val in enumerate(sol) if val]) # composition de la solution