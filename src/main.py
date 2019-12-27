import math
import random
import copy
import time

import file_parsing
import local_search
import incremental_elicitation
import nd_tree
import interactive_local_search
##### Paramètres du programme #####

# n objets, entre 1 et 200
n = 10
k = math.floor(n/2)
# p critères, entre 1 et 6
p = 5

# on crée un vecteur de poids aléatoire simulant les préférences du décideur
w = [random.uniform(0, 1) for i in range(p)]

# on le normalise pour que la somme du vecteur fasse 1
w = [w[i] / sum(w) for i in range(p)]


####################################

def procedure1_PLS():
    data = file_parsing.get_data(n,p) # n: nb de objets; p: nb de criteres

    print("Recherche locale:\n\n")
    time1 = time.time()

    [allx, ally] = local_search.neighbor_local_search(n, k, p, data)
    time2 = time.time()
    ally_for_file = copy.deepcopy(ally)

    #print("Données utilisées: ", data)
    #print("Vecteurs d'affectation solutions: ", allx)
    #print("Valeurs des évaluations: ", ally)

    print("\n\nElicitation incrémentale:\nNombre de solutions potentielles:", len(ally), "\n\n")
    time3 = time.time()

    evidence = [];
    [opt, opt_value, nb_q, _, _] = incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, evidence)

    time4 = time.time()
    print("Solution optimale: ", opt)
    print("Valeur de la solution: ", opt_value)
    print("Poids du décideur: ", w)
    print("Nombre de questions: ", nb_q)

    file_parsing.write_res_proc1_PLS(ally_for_file, n, p, nb_q, time2 - time1, time4 - time3)

def procedure1_nd_tree():
    data = file_parsing.get_data(n, p)

    print("Recherche locale:\n\n")
    time1 = time.time()

    [allx, ally] = nd_tree.nd_tree(n, k, p, data)
    time2 = time.time()
    ally_for_file = copy.deepcopy(ally)

    # print("Données utilisées: ", data)
    # print("Vecteurs d'affectation solutions: ", allx)
    # print("Valeurs des évaluations: ", ally)

    print("\n\nElicitation incrémentale:\nNombre de solutions potentielles:", len(ally), "\n\n")
    time3 = time.time()

    [opt, opt_value, nb_q, _, _] = incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, [])

    time4 = time.time()
    print("Solution optimale: ", opt)
    print("Valeur de la solution: ", opt_value)
    print("Poids du décideur: ", w)
    print("Nombre de questions: ", nb_q)

    file_parsing.write_res_proc1_nd_tree(ally_for_file, n, p, nb_q, time2 - time1, time4 - time3)

def procedure2_interactive_local_search():
    data = file_parsing.get_data(n,p) # n: nb de objets; p: nb de criteres

    print("Recherche locale + Elicitation incrementale:\n\n")
    time1 = time.time()

    opt, opt_value, nb_q = interactive_local_search.interactive_local_search(n, k, p, data,w)

    time2 = time.time()
    print("Solution optimale: ", opt)
    print("Valeur de la solution: ", opt_value)
    print("Poids du décideur: ", w)
    print("Nombre de questions: ", nb_q)

    file_parsing.write_res_proc2_ILS([opt], n, p, nb_q, time2 - time1)

t = time.time()
procedure1_PLS();
t1 = time.time()
procedure1_nd_tree()
t2 = time.time()
procedure2_interactive_local_search();
t3 = time.time()


print("PLS {}".format(t1-t))
print("nb_tree {}".format(t2-t1));
print("ILS {}".format(t3-t2))


