# -*- coding: utf-8 -*-

import gurobipy as gp
from gurobipy import GRB

def computePMR(x,y,evidence):

    #########################
    ####### initialization du model
    ####################
    m = gp.Model("Pairwise Max Regret")
    m.setParam("OutputFlag",0)

    ##########################
    ######  declaration des variables
    ##########################
    w=[]
    for i in range(len(x)):
        w.append(m.addVar(vtype=GRB.CONTINUOUS))

    ###########################
    #### ajout des contraintes
    ###########################
    # cst : evidence
    for a,b in evidence:
        expr1 = gp.LinExpr();
        expr2 = gp.LinExpr();
        for i in range(len(w)):
            expr1.addTerms(a[i], w[i]);
            expr2.addTerms(b[i], w[i]);
        m.addConstr(expr1 >= expr2);
    # cst 
    for i in range(len(w)):
        m.addConstr(w[i] >= 0)
    # cst : um (w[i],i=1..n) = 1
    m.addConstr(gp.quicksum(w[i] for i in range(len(w))) <= 1)

    #########################
    ###### def de l'objectif
    ##########################

    m.setObjective(gp.quicksum(w[i] * y[i] for i in range(len(w))) - gp.quicksum(w[i] * x[i] for i in range(len(w))), GRB.MAXIMIZE)

    ####################
    ########  resolution
    ####################

    m.optimize()
    

    obj = m.getObjective()

    return obj.getValue() # valeur trouver
