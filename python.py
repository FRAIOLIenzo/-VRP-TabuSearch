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
        {i: random.randint(1, poids_max) for i in range(nb_objets)} #SOLUTION
    valeur_objets =\
        {i: random.randint(1, val_max) for i in range(nb_objets)}   #SOLUTION
                                                                    #SOLUTION
    return poids_objets, valeur_objets                              #SOLUTION

def random_solution():
    sac = tuple(random.choice([False, True]) for _ in range(nb_objets)) #SOLUTION
                                                                        #SOLUTION
    while (poids_contenu(sac) > capacite):                              #SOLUTION
        objets_presents = tuple(                                        #SOLUTION
            i for i, val in enumerate(sac) if val)                      #SOLUTION
        objet_supprime = random.choice(objets_presents)                 #SOLUTION
        sac = sac[:objet_supprime] + (False,) + sac[objet_supprime+1:]  #SOLUTION
                                                                        #SOLUTION
    return sac                                                          #SOLUTION

@lru_cache(maxsize=None)
def poids_contenu(sac):
    """
    Cette fonction renvoie la somme des poids des objets dans le sac
    """
    return sum(poids_objets[i] for i, val in enumerate(sac) if val) #SOLUTION

@lru_cache(maxsize=None)
def valeur_contenu(sac):
    """
    Cette fonction renvoie la somme des valeurs des objets dans le sac
    """
    return sum(valeur_objets[i] for i, val in enumerate(sac) if val) #SOLUTION

@lru_cache(maxsize=None)
def voisinage(sac):
    voisins = []                                                     #SOLUTION
    for k in range(len(sac)):                                        #SOLUTION
        voisin = sac[:k] + (not(sac[k]),) + sac[k+1:]                #SOLUTION
        if (poids_contenu(voisin) <= capacite):                      #SOLUTION
            voisins.append(voisin)                                   #SOLUTION
    return voisins                                                   #SOLUTION

def recherche_tabou(solution_initiale, taille_tabou, iter_max):
    """
    1. On part d'un élément de notre ensemble de recherche qu'on déclare élément courant
    2. On considère le voisinage de l'element courant et on choisit le  meilleur d'entre
       eux comme nouvel element courant, parmi ceux absents de la liste tabou, et on l'ajoute
       a la liste tabou
    3. On boucle jusqu'a condition de sortie.
    """
    nb_iter = 0                                                                #SOLUTION
    liste_tabou = deque((), maxlen = taille_tabou)                             #SOLUTION
                                                                               #SOLUTION
    # variables solutions pour la recherche du voisin optimal non tabou        #SOLUTION
    solution_courante = solution_initiale                                      #SOLUTION
    meilleure = solution_initiale                                              #SOLUTION
    meilleure_globale = solution_initiale                                      #SOLUTION
                                                                               #SOLUTION
    # variables valeurs pour la recherche du voisin optimal non tabou          #SOLUTION
    valeur_meilleure = valeur_contenu(solution_initiale)                       #SOLUTION
    valeur_meilleure_globale = valeur_meilleure                                #SOLUTION
                                                                               #SOLUTION
    while (nb_iter < iter_max):                                                #SOLUTION
        valeur_meilleure = -1                                                  #SOLUTION
                                                                               #SOLUTION
        # on parcourt tous les voisins de la solution courante                 #SOLUTION
        for voisin in voisinage(solution_courante):                            #SOLUTION
            valeur_voisin=valeur_contenu(voisin)                               #SOLUTION
                                                                               #SOLUTION
            # MaJ meilleure solution non taboue trouvée                        #SOLUTION
            if valeur_voisin > valeur_meilleure and voisin not in liste_tabou: #SOLUTION
                valeur_meilleure = valeur_voisin                               #SOLUTION
                meilleure = voisin                                             #SOLUTION
                                                                               #SOLUTION
        # on met à jour la meilleure solution rencontrée depuis le début       #SOLUTION
        if valeur_meilleure > valeur_meilleure_globale:                        #SOLUTION
            meilleure_globale = meilleure                                      #SOLUTION
            valeur_meilleure_globale = valeur_meilleure                        #SOLUTION
            nb_iter = 0                                                        #SOLUTION
        else:                                                                  #SOLUTION
            nb_iter += 1                                                       #SOLUTION
                                                                               #SOLUTION
        # on passe au meilleur voisin non tabou trouvé                         #SOLUTION
        solution_courante = meilleure                                          #SOLUTION
                                                                               #SOLUTION
        # on met à jour la liste tabou                                         #SOLUTION
        liste_tabou.append(solution_courante)                                  #SOLUTION
                                                                               #SOLUTION
    return meilleure_globale                                                   #SOLUTION

nb_objets = 100
capacite = 20
random.seed(a=3)
poids_objets, valeur_objets = random_objets(10, 10)
sac = (False,)*nb_objets

print("tabou de taille 5")
sol = recherche_tabou(sac, taille_tabou=5, iter_max=30)
print("valeur finale = " + str(valeur_contenu(sol)) + ", capacite="+str(poids_contenu(sol)) + "/" + str(capacite))
print([i for i, val in enumerate(sol) if val]) # composition de la solution