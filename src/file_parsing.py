
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

def get_pareto(n,p):
    with open('../Fronts de Pareto/PF_'+str(n)+'_'+str(p)+'.txt','r') as f:
        pareto = [[int(num) for num in line.split(' ')] for line in f]
    return pareto

def write_res_proc2_ILS(opt, real_opt, n, p, w, nb_q, time):
    with open('../res/ILS_'+str(n)+'_'+str(p)+'.txt', 'a+') as f:
        f.write('Temps d\'execution : '+ str(round(time,6))+'\n')
        f.write("gap: " + str(round((real_opt-opt)/real_opt,6))+'\n')
        f.write('Jeu de poids: ')
        for v in w:
            f.write(str(v)+" ")
        f.write("\n")
        f.write('Nombre de questions: '+ str(nb_q)+'\n')
def write_res_proc1_PLS(opt, real_opt, n, p, w, nb_q, time_PLS, time_IE):
    with open('../res/PLS_'+str(n)+'_'+str(p)+'.txt', 'a+') as f:
        f.write('Temps d\'execution: '+ str(round(time_PLS+time_IE,6))+'\n')
        f.write("gap: " + str(round((real_opt-opt)/real_opt,6))+'\n')
        f.write('Temps d\'execution de la recherche locale: '+ str(round(time_PLS,2))+'\n')
        f.write('Temps d\'execution de l\'elicitation incrementale: '+ str(round(time_IE,2))+'\n')
        f.write('Jeu de poids: ')
        for v in w:
            f.write(str(v)+" ")
        f.write("\n")
        f.write('Nombre de questions: '+ str(nb_q)+'\n')

def write_res_proc1_nd_tree(opt, real_opt, n, p, w, nb_q, time_PLS, time_IE):
    with open('../res/ND_'+str(n)+'_'+str(p)+'.txt', 'a+') as f:
        f.write('Temps d\'execution: '+ str(round(time_PLS+time_IE,6))+'s\n')
        f.write("gap: " + str(round((real_opt-opt)/real_opt,6))+'\n')
        f.write('Temps d\'execution de la recherche locale: '+ str(round(time_PLS,2))+'\n')
        f.write('Temps d\'execution de l\'elicitation incrementale: '+ str(round(time_IE,2))+'\n')
        f.write('Jeu de poids: ')
        for v in w:
            f.write(str(v)+" ")
        f.write("\n")
        f.write('Nombre de questions: '+ str(nb_q)+'\n')
