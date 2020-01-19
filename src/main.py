import math
import random
import copy
import time

import file_parsing
import local_search
import incremental_elicitation
import nd_tree
import interactive_local_search
import time
import multiprocessing

def compare_to_file(n,p,k):
    pareto = file_parsing.get_pareto(n,p)
    pareto_opt=pareto[0]
    pareto_opt_value=0
    for i in range(p):
        pareto_opt_value+=pareto_opt[i]*w[i]
    for par in pareto:
        pareto_value=0
        for i in range(p):
            pareto_value += par[i] * w[i]
        if pareto_value>pareto_opt_value:
            pareto_opt=par
            pareto_opt_value=pareto_value
    return pareto_opt


def procedure1_PLS(n,p,k,w,start_time):
    print("procedure1_PLS  n={} p={}".format(n,p))
    data = file_parsing.get_data(n,p) # n: nb de objets; p: nb de criteres

    # print("Recherche locale:\n\n")
    time1 = time.time()

    [allx, ally] = local_search.neighbor_local_search(n, k, p, data)
    time2 = time.time()
    ally_for_file = copy.deepcopy(ally)

    #print("Données utilisées: ", data)
    #print("Vecteurs d'affectation solutions: ", allx)
    #print("Valeurs des évaluations: ", ally)

    # print("\n\nElicitation incrémentale:\nNombre de solutions potentielles:", len(ally), "\n\n")
    time3 = time.time()

    evidence = [];
    [opt, opty, opt_value, nb_q, _, _] = incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, evidence)

    time4 = time.time()
    # print("Solution optimale: ", opt)
    # print("Valeur de la solution: ", opt_value)
    # print("Poids du décideur: ", w)
    # print("Nombre de questions: ", nb_q)

    real_opt=compare_to_file(n, p, k)
    real_opt = sum(w[i]*real_opt[i] for i in range(len(w)))
    file_parsing.write_res_proc1_PLS(opt_value, real_opt, n, p, w, nb_q, time2 - time1, time4 - time3)
    
    print("END procedure1_PLS  n={} p={} time={}".format(n,p,time.time()))
    return
def procedure1_nd_tree(n,p,k,w,start_time):

    print("procedure1_ND_tree  n={} p={}".format(n,p))
    data = file_parsing.get_data(n, p)

    # print("Recherche locale:\n\n")
    time1 = time.time()

    [allx, ally] = nd_tree.nd_tree(n, k, p, data)
    time2 = time.time()
    ally_for_file = copy.deepcopy(ally)

    # print("Données utilisées: ", data)
    # print("Vecteurs d'affectation solutions: ", allx)
    # print("Valeurs des évaluations: ", ally)

    # print("\n\nElicitation incrémentale:\nNombre de solutions potentielles:", len(ally), "\n\n")
    time3 = time.time()

    [opt, opty, opt_value, nb_q, _, _] = incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, [])

    time4 = time.time()
    # print("Solution optimale: ", opt)
    # print("Valeur de la solution: ", opt_value)
    # print("Poids du décideur: ", w)
    # print("Nombre de questions: ", nb_q)

    real_opt = compare_to_file(n, p, k)
    real_opt = sum(w[i]*real_opt[i] for i in range(len(w)))
    
    file_parsing.write_res_proc1_nd_tree(opt_value, real_opt, n, p, w, nb_q, time2 - time1, time4 - time3)
    print("ND procedure2_ILS  n={} p={} time={}".format(n,p,time.time()-start_time))
    return
def procedure2_interactive_local_search(n,p,k,w,start_time):
    print("START procedure2_ILS  n={} p={}".format(n,p))
    data = file_parsing.get_data(n,p) # n: nb de objets; p: nb de criteres

    # print("Recherche locale + Elicitation incrementale:\n\n")

    time1 = time.time()

    opt,opt_solution, opt_value, nb_q = interactive_local_search.interactive_local_search(n, k, p, data,w)

    time2 = time.time()
    #print("Solution optimale: ", opt)
    # print("Valeur de la solution: ", opt_value)
    # print("Poids du décideur: ", w)
    # print("Nombre de questions: ", nb_q)

    real_opt = compare_to_file(n, p, k)
    real_opt = sum(w[i]*real_opt[i] for i in range(len(w)))
    
    file_parsing.write_res_proc2_ILS(opt_value, real_opt, n, p, w, nb_q, time2 - time1)
    
    print("END procedure2_ILS  n={} p={} time={}".format(n,p,time.time()-start_time))
    return
if __name__ == "__main__":

    # n objets, entre 1 et 200
    parametres = [[10,2],[10,3],[10,4],[10,5],[20,3],[20,4]];
    para_ILS = [[20,5],[30,4],[30,5],[40,3],[40,4]];
    for n,p in para_ILS:
        k = math.floor(n/2)    
        data = file_parsing.get_data(n,p) # n: nb de objets; p: nb de criteres
        ###################################################
        ##### MEME W POUR TROIS ALGO!
        ######################################################
        # on crée un vecteur de poids aléatoire simulant les préférences du décideur
        w = [random.uniform(0, 1) for i in range(p)]
        # on le normalise pour que la somme du vecteur fasse 1
        w = [w[i] / sum(w) for i in range(p)]
    
        for i in range(4):
            procedure2_interactive_local_search(n,p,k,w,time.time())
        #procedure1_PLS(n,p,k,w,time.time());
#        for i in range(4):
#            procedure1_nd_tree(n,p,k,w,time.time());      
