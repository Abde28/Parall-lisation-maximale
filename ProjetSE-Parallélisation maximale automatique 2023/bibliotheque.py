import numpy as np # travaille sur les tableaux et le calcule scientifique
import threading #  parallélisme basé sur les Threads
import time
import networkx as nx # étude de graphe et réseaux
import matplotlib.pyplot as plt # tracer et visualiser des graphiques 2D

"""Définition de la classe "Task" : Cette classe représente une tâche dans un système de tâches."""
class Task :
    name = ""
    reads = [ ]
    writes = [ ]
    dependence  = [ ]
    children = [ ]
    run = None

    def __init__ ( self) :
        self.name
        self.reads
        self.writes
        self.dependence
        self.children
        self.run
    def __init__ ( self , name , reads , writes , dependance ,children ,run) :
       self.name=name
       self.reads= reads
       self.writes = writes
       self.dependence =dependance
       self.children =children
       self.run=run

    def compar_name ( self , T ) :
        if self.name == T.name :
            return True

    """Méthode "task_indep" :
    Cette méthode vérifie l'indépendance entre deux tâches en vérifiant s'il existe un chemin  entre elles dans le graphe de précédence du système de tâches."""
    def task_indep ( self , T , Task_sys) :
       if Task_sys.find_path (  self.name , T.name ) or Task_sys.find_path2 (  self.name , T.name ) :
           return False
       else : return True

    """Méthode "bern_verif" : Cette méthode vérifie si les conditions de Bernstein sont valides pour deux tâches données."""
    def bern_verif ( self , T ) :
        intersecRW = [ x for x in T.writes if x in self.reads ]
        intersecWR = [ x for x in T.reads if x in self.writes ]
        intersecWW = [ x for x in T.writes if x in self.writes ]

        if (intersecRW == [ ] and intersecWR == [ ] and intersecWW == [ ]) :
            return True
        else :
            return False

"""Définition de la classe "TaskSystem" : Cette classe représente un système de tâches."""
class TaskSystem :
    tasks: Task = [ ]
    tasks_prec = dict ( )
    tasks_nexts= dict ( )

    def __init__ ( self , task ) :
        self.tasks = list (set ( task ))
     # les dictionnaire de précédance et de descendance sont généré à partir de la listes de tâches
        for t in self.tasks :
            dep=[]
            for d in t.dependence:
                dep.append(d)
            self.tasks_prec [t.name] = dep
        self.tasks_prec= dict(sorted(self.tasks_prec.items()))

        for ta in self.tasks :
            next=[]
            for c in ta.children:
                next.append(c)
            self.tasks_nexts [ ta.name ] = next
        self.tasks_nexts = dict(sorted(self.tasks_nexts.items()))

    """Méthode "system_valid" : 
    Cette méthode vérifie si le système de tâches est valide en vérifiant si les noms des tâches sont uniques et s'ils existent dans la liste des tâches
     on compare d'abord les tailles de la liste et du dictionnaire de précédance."""
    def system_valid ( self ) :
        global name_exist , name_dup
        valid = True
        if len ( self.tasks ) == len ( self.tasks_prec ) :
            for k in self.tasks_prec :
                for e in self.tasks :
                    if e.name != k :
                        name_exist = False
                    else :
                        name_exist = True
                        break
                if not name_exist : break
            for t in self.tasks :
                name_dup = False
                for ta in self.tasks :
                    if ta != t and t.compar_name ( ta ) :
                        name_dup = True
                        break
                if name_dup : break
            valid = (name_exist and not name_dup)
            return valid

        elif len ( self.tasks ) < len ( self.tasks_prec ) :
            print ( "le dictionnaire de précédence contient des noms de tâches inexistantes !!!!" )
            return valid
        else :
            print ( "La liste des taches contient des noms dupliqués !!!!" )
            return valid

    """  Méthode "find_path":
     Cette méthode retourne un chemin entre deux tâches origine et destination dans le graphe du système de tache si il exist en parcourant le dict de descendance."""
    def find_path ( self , start , end , path=[ ] ) :
        graph = self.tasks_nexts
        path = path + [ start ]
        if start == end :
            return path
        if not start in graph.keys() :
            return None
        for node in graph [ start ] :
            if node not in path :
                newpath = self.find_path (  node , end , path )
                if newpath :
                    return newpath
        return None

    """  Méthode "find_path2" : 
     fait la meme chose que le "find_path" mais cette fois si on parcourant le dict de précédance.
     En utilisant les deux fonctions "find_path" et "find_path2" simultanémant  on peut vérifier l'existance d'un chemin dans les deux sens """
    def find_path2 ( self , start , end , path=[ ] ) :
        graphe = self.tasks_prec
        path = path + [ start ]
        if start == end :
            return path
        if not start in graphe.keys() :
            return None
        for node in graphe [ start ] :
            if node not in path :
                newpath = self.find_path2 (  node , end , path )
                if newpath :
                    return newpath
        return None

    """Méthode "system_det" :
    Cette méthode vérifie le déterminisme d'un système de tâches en vérifiant si pour toute paire de tâches indépendantes les conditions de Bernstein sont respectées."""
    def system_det ( self ) :

        for t in self.tasks :
            is_det = True
            for ta in self.tasks :
                if ta != t and ta.task_indep ( t, self ) :
                    bern = ta.bern_verif ( t )
                    if not bern :
                        is_det= False
                        break
            if not is_det : break
        return is_det

    """Méthode "clear_redundancy" : 
    Cette méthode élimine les flèches redondances  dans le graphe de précédence en utiliisant la matrices des chemins ."""
    def clear_redundancy( self,graphe ):
        graph=graphe
        key=list(graph.keys())
        M=np.zeros((len(graph),len(graph)))
        for t in graph:
            for ta in graph:
                if t<ta and ta in graph[t]:
                    M[key.index(t)][key.index(ta)]=1

        for i in range(len(graph)) :
            for j in range(len(graph)):
                if i < j and M[i][j]==1 :
                    for k in range(len(graph)):
                        if j!=k and i < k and M[i][k]==1 and M[j][k]==1 :
                            M[i][k] = 0

        for i in range(len(graph)):
            values = [ ]
            for j in range(len(graph)):
                if i < j and M[i][j] == 1:
                    values.append(key[j])
            graph[key[i]]= values

        return  graph

    """  Méthode "par_max" :
     Cette méthode applique  l'algorithme de parallélisme maximal sur un système de tâches"""
    def par_max (self):
        graph_par_max = dict ( )
        #vérification du determinisme
        if(self.system_det()):
          #  construction du système de parallélisme maximal
            for t in self.tasks:
               depp=[]
               for ta in self.tasks:
                if t.name < ta.name and not t.task_indep(ta , self) and not t.bern_verif(ta) :
                    depp.append(ta.name)
                graph_par_max[t.name]= depp

            # élimination de la redondance
            graph_par_max= dict ( sorted ( graph_par_max.items ( ) ) )
            self.tasks_nexts = self.clear_redundancy(graph_par_max)

            # mise à jour du dictionnaire de précédance et du dict de descendance
            for k in graph_par_max.keys():
                val=[]
                for l in graph_par_max.keys():
                    if k!=l and k in graph_par_max[l]:
                        val.append(l)
                self.tasks_prec[k]= val

            return self.tasks_nexts

        else :  print("le système est indeterminé !!!!")


    """  Méthode "getDependencies" :
     Cette méthode pour un nom de tâche donné renvoie la liste de ses dependances"""
    def getDependencies ( self , name ) :
        if name in self.tasks_prec :
            return self.tasks_prec [ name ]
        else :
            return None

    """EXECUTION SEQUENTIELLE des tâches du système"""
    def runSeq( self ):

        global queue
        queue = []
        n_queue=[]
        # génération d'une file de priorité d'éxecution à partir du dict de précedance
        while len(queue) != len(self.tasks) :
            for t in self.tasks :
                valid = True
                for p in self.tasks_prec[t.name]:
                    for q in range (len(queue)):
                        n_queue.append(queue[q].name)
                    if p not in n_queue:
                        valid= False
                        break
                if valid:
                    queue.append(t)
                    buff = [ ]
                    for e in queue :
                        if e not in buff:
                            buff.append ( e )
                    queue = buff

        start = time.time ( )
        # lancement de l'éxecution
        for i in range(len(queue)):
            queue[i].run()
        # Calcul du temps d'éxecution
        t_ex = time.time ( ) - start
        return t_ex

    """EXECUTION SEQUENTIELLE des tâches du système"""
    def runPar ( self ):
        # creation d'une liste de threads
        MyThread = [ ]
        # dict de descendance par niveau
        level_tree = dict ( )
        v = [ ]
        Key = 0
        # créer un thread pour chaque tache dans le système
        for t in self.tasks :
            MyThread.append ( threading.Thread ( target=t.run , name=t.name ) )
        # génération du niveau 0 du level_tree
        for th in MyThread :
            if self.tasks_prec[th.name]==[]:
                v.append(th)
                MyThread.remove(th)
        # génération du reste du dictionnaire à partir du niv 0
        level_tree[Key]=v
        while MyThread!=[]:
            v = [ ]
            for x in level_tree [ Key ] :
                for th in MyThread :
                    if th.name in self.tasks_nexts [ x.name ] and th not in v :
                        v.append ( th )
                for y in v :
                    if y in MyThread :
                        MyThread.remove ( y )

            Key += 1
            level_tree [ Key ] = v
            print ( level_tree , MyThread )

        start = time.time ( )
        # lancement de l'éxecution
        for k in level_tree.keys():
            for val in level_tree[k]:
                val.start()
            for val in level_tree[k]:
                val.join()
        # Calcul du temps d'éxecution
        t_ex = time.time ( ) - start
        return t_ex



    """Cette méthode calcule le coût du parrallélisme en comparant les temps d'éxecutions de runSeq() et runPar()
    et Calcule aussi la moyenne des temps d'éxecutions"""
    def parCost( self ):
        seq_t=0
        par_t=0
        select = int(input(">>> parallèle d'abord [1] sinon [0] ?\n>>> "))
        moy= int(input(">>> voulez-vous la moyenne [1] sinon [0] ?\n>>> "))
        if select==1:
            if moy == 1 :
                limit = int ( input ( ">>> Combien d'execution ?\n>>> " ) )
                for i in range ( limit ) :
                    par_t += self.runPar ( ) / limit
                    seq_t += self.runSeq ( ) / limit
                else :
                    par_t = self.runPar ( )
                    seq_t = self.runSeq ( )
        else:
            if moy == 1 :
                limit = int ( input ( ">>> Combien d'execution ?\n>>> " ) )
                for i in range ( limit ) :
                    seq_t += self.runSeq ( ) / limit
                    par_t += self.runPar ( ) / limit
                else :
                    seq_t = self.runSeq ( )
                    par_t = self.runPar ( )



        print(seq_t ,par_t)
        cout= seq_t-par_t
        return print(cout)



    def draw ( self ) :

        # Création d'un graphe dirigé
        G = nx.DiGraph ( )

        # Ajout des tâches comme nœuds
        for t in self.tasks :
            G.add_node ( t.name )
            for ta in self.tasks :
                if t.name != ta.name and ta.name in self.tasks_nexts [ t.name ] :
                    G.add_edge ( t.name , ta.name )

        ordre_topologique = list ( nx.topological_sort ( G ) )

        # Créer un dictionnaire pour stocker les niveaux d'étage de chaque nœud
        niveaux = {}

        # Parcourir les nœuds dans l'ordre topologique et attribuer les niveaux d'étage
        for tache in ordre_topologique :
            niveau_max = 0  # Niveau d'étage maximum des nœuds prédécesseurs
            for predecesseur in G.predecessors ( tache ) :
                if predecesseur in niveaux :
                    niveau_max = max ( niveau_max , niveaux [ predecesseur ] )
            niveaux [ tache ] = niveau_max + 1

        # Organiser les nœuds dans le graphe en fonction de leurs niveaux d'étage
        pos = {}  # Dictionnaire pour stocker les positions des nœuds
        for tache in niveaux :
            niveau = niveaux [ tache ]
            if niveau not in pos :
                pos [ niveau ] = {}  # Créer un sous-dictionnaire pour chaque niveau d'étage
            pos [ niveau ] [ tache ] = (len ( pos [ niveau ] ) ,
                                        -niveau)  # Organiser les nœuds dans l'ordre du niveau d'étage et inverser la position en y pour afficher de haut en bas

        # Appliquer la position des nœuds pour chaque niveau d'étage
        pos_final = {}
        for niveau in pos :
            pos_final.update ( pos [ niveau ] )

        # Dessiner le graphe avec une disposition verticale
        nx.draw ( G , pos_final , with_labels=True , node_size=1000 , node_color='lightblue' , font_size=12 ,
                  font_color='black' , font_weight='bold' , arrowsize=15 , arrowstyle='->' , width=2 , node_shape='s' ,
                  verticalalignment='center' )
        plt.show ( )