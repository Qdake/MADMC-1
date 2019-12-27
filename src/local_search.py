import random
import copy

def neighbor_local_search(n,k,p,data):

    # Parameters
    # ----------
    # n : int.
    #     nb d'objects.
    # k : int.
    #     nb d'objects à choisir.
    # p : int
    #     nb de criteres.
    # data : int[n][p]
    #     tous les objects.

    # Returns
    # -------
    # front_pareto, eval des elements

    def create_random_solution():
        x = [0] * n
        # on récupère k valeur aléatoire entre 0 et n-1
        v = random.sample(range(0, n - 1), k)

        # on met x[i] à 1 pour les valeurs aléatoires précédentes
        i = 0
        while i < k:
            x[v[i]] = 1
            i += 1
        return x

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

    # création d'un vecteur aléatoire et calcule de son évaluation
    x = create_random_solution()
    y = compute_evaluation(x)

    # création de listes pour stocker nos solutions et leur évaluation
    allx = []
    allx.append(x)
    ally = []
    ally.append(y)

    # recherche du voisinage de x, les voisins et leurs evaluations sont stockes dans allx et ally
    neighbors(x, allx, ally)

    # on supprime les solutions dominées
    compute_dominance(allx, ally)

    prev_allx = []
    while sorted(prev_allx) != sorted(allx):
        prev_allx = copy.deepcopy(allx)
        for x in allx:
            neighbors(x, allx, ally)    # recherche du voisinage de x, les voisins et leurs evaluations sont stockes dans allx et ally
        compute_dominance(allx, ally)       # on supprime les solutions dominées

    return [allx,ally]
