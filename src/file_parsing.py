
def get_data(n,p):
    # récupère les données du fichier
    with open('../data.txt', 'r') as f:
        data = [[int(num) for num in line.split(' ')] for line in f]

    # print(data)

    # On ne garde que les n premiers objets
    data = data[:(n - 200)]

    # on ne grarde que les p premiers critères par objet
    i = 0
    while i < len(data):
        data[i] = data[i][:p - 6]
        i += 1
    return data
    # print(data)

def write_res_proc2_ILS(ally, n, p, nb_q, time):
    with open('../res/results_proc2_ils_'+str(n)+'_'+str(p), 'a+') as f:
        f.truncate(0)
        f.write('Temps d\'execution : '+ str(round(time,2))+'s\n')
        f.write('Nombre de questions: '+ str(nb_q)+'\n')
        f.write('Nombre de Pareto: '+ str(len(ally))+'\n')
        for y in ally:
            for v in y:
                f.write(str(v)+" ")
            f.write('\n')

def write_res_proc1_PLS(ally, n, p, nb_q, time_PLS, time_IE):
    with open('../res/results_proc1_pls_'+str(n)+'_'+str(p), 'a+') as f:
        f.truncate(0)
        f.write('Temps d\'execution de la recherche locale: '+ str(round(time_PLS,2))+'s\n')
        f.write('Temps d\'execution de l\'elicitation incrementale: '+ str(round(time_IE,2))+'s\n')
        f.write('Nombre de questions: '+ str(nb_q)+'\n')
        f.write('Nombre de Pareto: '+ str(len(ally))+'\n')
        for y in ally:
            for v in y:
                f.write(str(v)+" ")
            f.write('\n')

def write_res_proc1_nd_tree(ally, n, p, nb_q, time_PLS, time_IE):
    with open('../res/results_proc1_nb_tree_'+str(n)+'_'+str(p), 'a+') as f:
        f.truncate(0)
        f.write('Temps d\'execution de la recherche locale: '+ str(round(time_PLS,2))+'s\n')
        f.write('Temps d\'execution de l\'elicitation incrementale: '+ str(round(time_IE,2))+'s\n')
        f.write('Nombre de questions: '+ str(nb_q)+'\n')
        f.write('Nombre de Pareto: '+ str(len(ally))+'\n')
        for y in ally:
            for v in y:
                f.write(str(v)+" ")
            f.write('\n')