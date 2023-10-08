from bibliotheque import *


M1=0
M2=0
M3=0
M4=0
M5=0
M6=0

def runT1():
        global M1,M4
        M4 = abs(7*M1-12)
        print ( "le resultat de la tache T1 est : {}".format (M4) )
        print ( "M1=",M1 , "M2=",M2 ,"M3=",M3 , "M4=",M4 , "M5=",M5 , "M6=",M6 ,"\n")


def runT2():
        global M1,M3,M4
        M1 = M3+M4
        print ( "le resultat de la tache T2 est : {}".format (M1) )
        print ( "M1=",M1 , "M2=",M2 ,"M3=",M3 , "M4=",M4 , "M5=",M5 , "M6=",M6 ,"\n")


def runT3():
        global M5,M3,M4
        M5 = M3*M4
        print ( "le resultat de la tache T3 est : {}".format (M5) )
        print ( "M1=",M1 , "M2=",M2 ,"M3=",M3 , "M4=",M4 , "M5=",M5 , "M6=",M6 ,"\n")


def runT4():
        global M2,M4
        M2 = 3*M4/2
        print ( "le resultat de la tache T4 est : {}".format (M2) )
        print ( "M1=",M1 , "M2=",M2 ,"M3=",M3 , "M4=",M4 , "M5=",M5 , "M6=",M6 ,"\n")


def runT5() :
        global M5
        M5+=1
        print ( "le resultat de la tache T5 est : {}".format (M5) )
        print ( "M1=",M1 , "M2=",M2 ,"M3=",M3 , "M4=",M4 , "M5=",M5 , "M6=",M6 ,"\n")


def runT6():
        global M1,M2,M4
        M4 += 5*M1-2*M2
        print ( "le resultat de la tache T6 est : {}".format (M4) )
        print ( "M1=",M1 , "M2=",M2 ,"M3=",M3 , "M4=",M4 , "M5=",M5 , "M6=",M6 ,"\n")


t1 = Task("T1",["M1"],["M4"],[],["T2","T3"],runT1)
t2 = Task("T2",["M3","M4"],["M1"], ["T2","T3"] ,["T4"],runT2)
t3 = Task("T3",["M3","M4"],["M5"],["T1"],["T4","T5"],runT3)
t4 = Task("T4",["M4"],["M2"],["T2","T3"],["T6"],runT4)
t5 = Task("T5",["M5"],["M5"],["T3"],["T6"],runT5)
t6 = Task("T6",["M1","M2"],["M4"],["T4","T5"],[],runT6)

List = []
List.append(t1)
List.append(t2)
List.append(t3)
List.append(t4)
List.append(t5)
List.append(t6)

s1 = TaskSystem(List)
t_name=[]
for t in s1.tasks:
        t_name.append(t.name)
#print(sorted(t_name))
#print(s1.tasks_prec,"\n")
#print(s1.tasks_nexts,"\n\n")

s1.par_max()
#print(s1.tasks_prec,"\n")
#print(s1.tasks_nexts)
#s1.parCost()
s1.draw()
#s1.runSeq()
#s1.runPar()

















 




