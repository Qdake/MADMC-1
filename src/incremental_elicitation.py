import pairwise_max_regret

# la preference d'un decideur comme une boite noire
def query_Is_x_better_then_y(x,y,w):
    
    scorex = 0
    scorey = 0
    
    # on calcule les scores des deux solutions x et y selon w
    for i in range(len(w)):
        scorex += x[i] * w[i]
        scorey += y[i] * w[i]
        
    #print("y - x avec le vecteur de poids du décideur (doit être inférieur à Min Max Regret",mmr,"): ", scorey - scorex)
    if scorex >= scorey:
        return True;
    else:
        return False;

def mmr_incremental_elicitaiton(allx, ally, w, evidence):
    
    mmr = 1
    opt = []
    opt_value = []
    nb_q = 0
    # on itère tant qu'on trouve un Min Max Regret > 0
    while (mmr > 0):

        # on calcule pour chaque paire le regret maximal
        pmr = []
        for i in range(len(ally)):
            temp_pmr = []
            for j in range(len(ally)):
                if i != j:
                    temp_pmr.append(pairwise_max_regret.computePMR(ally[i], ally[j],evidence))
                else:
                    temp_pmr.append(0)
            pmr.append(temp_pmr)
        #print("Pairwise Max Regrets: ", pmr)

        # on calcul à présent le regret maximal et argmax correspondant, pour chaque solution
        mr = [0] * len(pmr)
        argmax_mr = [0] * len(pmr)
        for i in range(len(pmr)):
            mr[i] = pmr[i][0]
            argmax_mr[i] = 0
            for j in range(1, len(pmr[i])):
                if mr[i] < pmr[i][j]:
                    mr[i] = pmr[i][j]
                    argmax_mr[i] = j
        #print("Max Regrets: ", mr)
        #print("Args Max Regret: ", argmax_mr)

        # on calcul le min max regret et l'argmin associé
        mmr = mr[0]
        argmin_mmr = 0

        for i in range(1, len(mr)):
            if mr[i] < mmr:
                mmr = mr[i]
                argmin_mmr = i

        #print("Min Max Regret: ", mmr)
        #print("Arg Min Max Regret: ", argmin_mmr)
        x = ally[argmin_mmr]
        y = ally[argmax_mr[argmin_mmr]]
        #print("x: ", ally[argmin_mmr], "y: ", ally[argmax_mr[argmin_mmr]])

        if (mmr > 0):
            nb_q+=1
            # on retire la solution qui n'est pas désirée par le décideur
            if query_Is_x_better_then_y(x,y,w):
                evidence.append([x,y])   # on obtient un fait: x est meilleur que y
                allx.pop(argmax_mr[argmin_mmr])
                ally.pop(argmax_mr[argmin_mmr])
            else:
                evidence.append([y,x]);  # on obtient un fait: y est meilleur que x
                allx.pop(argmin_mmr)
                ally.pop(argmin_mmr)
        else:
            opt = allx[argmin_mmr]
            opt_value = ally[argmin_mmr]
    return [opt, opt_value,nb_q, evidence, mr[0]]

