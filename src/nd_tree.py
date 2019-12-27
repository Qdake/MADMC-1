import random
import copy
import math

def nd_tree(n,k,p,data):

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

    def compute_dominance(nodes, newx, newy):
        potentialnode=0
        dist=0
        addnew = True
        for node in nodes:
            # on n'ajoute pas une solution déjà existant
            if newy in node["l_y"]:
                addnew = False
                return
            dom1n = 0
            dom2n = 0
            # si la solution est dominée par le point nadir du noeud courant, on ne l'ajoute nul part
            for k in range(p):
                if node["nadir"][k] < newy[k]:
                    dom2n += 1
                if node["nadir"][k] > newy[k]:
                    dom1n += 1
            if dom2n == 0 and dom1n > 0:
                return

            dom1i = 0
            dom2i = 0
            # si la solution domine le point idéal du noeud courrant, on remplace le noeud courant pas la solution
            for k in range(p):
                if node["ideal"][k] < newy[k]:
                    dom2i += 1
                if node["ideal"][k] > newy[k]:
                    dom1i += 1
            if dom1i == 0 and dom2i > 0:
                node["l_x"] = [newx]
                node["l_y"] = [newy]
                return

            # si le noeud idéal domine la solution OU que la solution domine le point nadir, on l'ajoute à ce noeud puis on s'arrête
            if (dom1i > 0 and dom2i == 0) or (dom1n ==0 and dom2n > 0):

                toremove = []
                for i in range(len(node["l_y"])):
                    dom1 = 0
                    dom2 = 0
                    # on calcul le nombre de fois où la nouvelle solution domine i, et le nombre de fois où i domine la nouvelle solution
                    for k in range(p):
                        if node["l_y"][i][k] < newy[k]:
                            dom2 += 1
                        if node["l_y"][i][k] > newy[k]:
                            dom1 += 1
                    # si i est strictement dominée, on les ajoute dans la liste des solutions à retirer
                    if dom1 == 0 and dom2 > 0:
                        toremove.append(i)
                    # si la nouvelle solution est dominée, on ne l'ajoute pas
                    if dom2 == 0 and dom1 > 0:
                        addnew = False
                        break
                # on retire toutes les solutions qui sont dominées par la nouvelle solution
                for i in reversed(toremove):
                    node["l_x"].pop(i)
                    node["l_y"].pop(i)
            # si la solution n'est pas dominées, on calcul la distance euclidienne au noeud courant
            if addnew:
                dist1=euclidean_dist(newy,node["l_y"])
                if dist==0 or dist1<dist:
                    dist=dist1
                    potentialnode=nodes.index(node)
        # on ajoute la nouvelle solution au noeud dont la distance euclidienne est la plus petite
        if addnew:
            nodes[potentialnode]["l_x"].append(newx)
            nodes[potentialnode]["l_y"].append(newy)
            nadir_ideal(nodes[potentialnode])

    def neighbors(nodes,node,x):
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
                        y1 = compute_evaluation(x1)
                        compute_dominance(nodes,x1,y1)
                        split(nodes)
                    j += 1
            i += 1

    def euclidean_dist(y,l_y):
        # calcul de la distance euclidienne entre une solution et un ensemble de solution
        dist = 0
        for y1 in l_y:
            dist+=sum((y[k] - y1[k]) ** 2 for k in range(p)) ** 0.5
        return dist

    def split(nodes):

        for node in nodes:
            # si le nombre de solution dans un noeud dépasse la limite:
            if len(node["l_y"])>node_size:
                # on calcul le nombre de nouveaux noeuds à faire
                nb_nodes=math.ceil(len(node["l_y"])/node_size)
                # on instancie les nouveaux noeuds
                newnodes=[]
                for a in range(nb_nodes):
                    newnodes.append({"ideal": 0, "nadir": 0, "l_x": [],"l_y": []})
                # pour chaque nouveau noeud, on ajoute une solution qui est la plus différente des autres
                for a in range(nb_nodes):
                    dist = 0
                    i = 0
                    # on calcul la solution qui est la plus loin des autres (au sens de la distance euclidienne)
                    for k in range(0, len(node["l_y"])):
                        dist1 = euclidean_dist(node["l_y"][k], node["l_y"])
                        if dist1 > dist:
                            dist = dist1
                            i = k
                    # on ajoute cette solution à un des nouveux noeuds
                    newnodes[a]["l_x"].append(node["l_x"][i])
                    newnodes[a]["l_y"].append(node["l_y"][i])
                    node["l_x"].pop(i)
                    node["l_y"].pop(i)

                # pour chaque solution restante dans le noeud
                # on les ajoute au nouveau noeud dont il est le plus proche de la première solution ajoutée dans ce noeud
                adds=[]
                for j in range(len(node["l_y"])):
                    dist = 0
                    i = 0
                    for a in range(0, len(newnodes)):
                        dist1 = euclidean_dist(node["l_y"][j], [newnodes[a]["l_y"][0]])
                        if dist1 > dist and len(newnodes[a]["l_y"])<node_size:
                            dist = dist1
                            i = a
                    adds.append((j,i))
                for (j,i) in adds:
                    newnodes[i]["l_x"].append(node["l_x"][j])
                    newnodes[i]["l_y"].append(node["l_y"][j])

                # on calcul la valeur du point nadir et ideal pour chaque nouveau noeud
                for newnode in newnodes:
                    nadir_ideal(newnode)
                    nodes.append(newnode)
                # on retire l'ancien noeud
                nodes.remove(node)


    def nadir_ideal(node):
        nadir = copy.deepcopy(node["l_y"][0])
        ideal = copy.deepcopy(node["l_y"][0])
        for i in range(1,len(node["l_y"])):
            for k in range(p):
                if node["l_y"][i][k] < nadir[k]:
                    nadir[k]=node["l_y"][i][k]
                if node["l_y"][i][k] > ideal[k]:
                    ideal[k]=node["l_y"][i][k]
        node["nadir"]=nadir
        node["ideal"]=ideal

    # création d'un vecteur aléatoire et calcule de son évaluation
    x = create_random_solution()
    y = compute_evaluation(x)

    node_size = 20

    # création de listes pour stocker nos noeuds
    nodes=[]
    node = {"ideal":y,"nadir":y,"l_x":[x],"l_y":[y]}
    nodes.append(node)
    # recherche du voisinage de x
    neighbors(nodes,node,node["l_x"][0])
    if len(nodes[0]["l_x"]) > node_size:
        split(nodes)
    for i in range(len(nodes)):
        nadir_ideal(nodes[i])
    prev_nodes = []
    # on boucle tant qu'on trouve de nouvelles solutions
    while prev_nodes != nodes:
        prev_nodes = copy.deepcopy(nodes)
        #on ajoute les voisins de chaque solution
        for node in nodes:
            for x in node["l_x"]:
                neighbors(nodes,node,x)
    allx=[]
    ally=[]
    for node in nodes:
        for y in node["l_y"]:
            ally.append(y)
        for x in node["l_x"]:
            allx.append(x)
    return [allx,ally]

