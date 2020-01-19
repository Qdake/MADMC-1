import random
import copy
import incremental_elicitation

def interactive_local_search(n,k,p,data,w):
    ################
    ### fonctions locales
    ###############
    def compute_evaluation(x):
        y = [0] * p
        j = 0
    
        # on fait ici une somme pour faire l'evaluation
        while j < p:
            i = 0
            while i < n:
                y[j] += x[i] * data[i][j]
                i += 1
            j += 1
        return y
    
    def create_starting_solution():
        ###############
        ### fonction locale
        ##############
        def find_best_objets(w):
            # calculer le score d'un objet selon w
            compute_score = lambda i: sum( [ data[i][j] * w[j] for j in range(len(w)) ] );
            # ordonner les objets selon leurs scores 
            index = list(range(len(data)));
            index_ordered = sorted( index , key = compute_score); # ordre croissant
            index_ordered = reversed(index_ordered);   # decroissant
            index_ordered = list(index_ordered)     # convertir a une liste
            x = [1 if i in index_ordered[:k] else 0 for i in list(range(len(data)))]; # on prend les k meilleurs objets
            return x # une solution
        
        ############
        ### main
        ############
        
        evidence = [];
        # parametre
        m = 2 * n;
        
        # Etape 1: on cree un ensemble de vecteur de poids aléatoire simulant les préférences du décideur
        ws = [];
        for i in range(m):   
            # on crée un vecteur de poids aléatoire simulant les préférences du décideur
            w = [random.uniform(0, 1) for i in range(p)] 
            # on le normalise pour que la somme du vecteur fasse 1
            w = [w[i] / sum(w) for i in range(p)]
            # on ajoute w dans ws
            ws.append(w);
        # Etape 2: pour chaque w trouver une solution optimale
        xs = [find_best_objets(w) for w in ws];  # pour chaque w trouver une solution optimale
        
        # Etape 3: find le most promising solution within xs
        allx = xs;
        ally = [compute_evaluation(x) for x in xs];
        compute_dominance(allx,ally)
        x, eval_x,_,nb_q, evidence, mr =  incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, evidence)
        
        return x, eval_x, evidence
    
    def compute_dominance(allx, ally):
        toremovex = []
        toremovey = []
        # on calcule les dominance pour chaque paire de solution i et j
        i = 0
        while i < len(allx):
            j = i + 1
            while j < len(ally):
                k = 0
                domi = 0
                domj = 0
                # on calcul le nombre de fois où j domine i, et le nombre de fois où i domine j
                while k < p:
                    if ally[i][k] < ally[j][k]:
                        domj += 1
                    if ally[i][k] > ally[j][k]:
                        domi += 1
                    k += 1
                # si une des solutions ne domine jamais l'autre strictement, elle est donc dominée faiblement
                # on l'ajoute à la liste des solutions à retirer
                # attention au cas où les évaluations sont égales!
                if domi == 0 and domj > 0 and allx[i] not in toremovex:
                    toremovex.append(allx[i])
                    toremovey.append(ally[i])
                    # print("i",i,j)
                if domj == 0 and domi > 0 and allx[j] not in toremovex:
                    toremovex.append(allx[j])
                    toremovey.append(ally[j])
                    # print("j",i,j)
                j += 1
            i += 1
        # on retire les elements dominés des listes allx et ally
        for x in toremovex:
            allx.remove(x)
        for y in toremovey:
            ally.remove(y)

    def compute_dominance2(allx, ally, newx, newy):
        toremove=[]
        addnew = True
        for i in range(len(ally)):
            dom1 = 0
            dom2 = 0
            # on calcul le nombre de fois où j domine i, et le nombre de fois où i domine j
            for k in range(p):
                if ally[i][k] < newy[k]:
                    dom2 += 1
                if ally[i][k] > newy[k]:
                    dom1 += 1
            if dom1 == 0 and dom2 > 0:
                toremove.append(i)
            if dom2 == 0 and dom1 > 0:
                addnew = False
        for i in reversed(toremove):
            allx.pop(i)
            ally.pop(i)
        if addnew:
            allx.append(newx)
            ally.append(newy)

    def neighbors(x, allx, ally):
        # on récupère les voisins de la manière suivante:
        # si la ième composante vaut 1 et la jème vaut 0
        # on fait une copie du vecteur et on met i à 0 et j à 1
        # on répète le procédé pour toutes les combinaisons de i et j possible
        i = 0
        while i < n:
            if x[i] == 1:
                j = 0
                while j < n:
                    if (x[j] == 0 and i != j):
                        x1 = copy.deepcopy(x)
                        x1[i] = 0
                        x1[j] = 1
                        # on n'ajoute pas de solution déjà existante dans notre ensemble
                        if (x1 not in allx):
                            y1 = compute_evaluation(x1)
                            #allx.append(x1)
                            #ally.append(y1)
                            compute_dominance2(allx,ally,x1,y1)
                    j += 1
            i += 1
            
    #######################
    ### MAIN : combinaison de LS et Incremental_elicitation
    #######################
            
    ######################
    ### Find a promising starting solution
    ######################
    # création d'un vecteur aléatoire et calcule de son évaluation
    x, eval_x, evidence = create_starting_solution()
    y = compute_evaluation(x)
    
    #######################
    ### Local improvement
    ######################
    improve = True;
    nb_q = 0;
    while improve:
        # création de listes pour stocker nos solutions et leur évaluation
        allx = []
        allx.append(x)
        ally = []
        ally.append(y)
    
        # recherche du voisinage de x
        neighbors(x, allx, ally)
    
        # on supprime les solutions dominées
        compute_dominance(allx, ally)

        newx, newy, eval_newx, new_nb_q, evidence, mr_x =  incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, evidence)
        nb_q += new_nb_q
        if mr_x > 0:
            x = newx
            y = newy
        else:
            improve = False
            opt_value = eval_newx
            
    return x,y, opt_value,nb_q
