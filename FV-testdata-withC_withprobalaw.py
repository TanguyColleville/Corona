
#################################################Modèle de Pandémie#########################################################
"""
Modèle empirique de la propagation d'un virus au sein d'une population
Simulation of the spread of a virus in Python. Use of POO to generate an individual population.
The likelihood of transmission of the virus and the intensity of movement of individuals are 
adjustable parameters. The time of recovery and the likelihood of survival depend on the age of the 
individual. It is also possible to house some of this population. An animation is done via Tkinter, 
and the individuals are modeled by colour circles that move within a frame; the blue ones are healthy, 
the green ones are healed, and the red ones are sick. At the end of the simulation the evolution 
curves of healthy, sick, dead, and healed individuals appear.

This project can be improved, it's only a first draft

"""
########################################################Les Modules#########################################################

import numpy as np
import random as rd
from tkinter import *
import matplotlib.pyplot as plt 

__author__ = "Colleville Tanguy"
__copyright__ = "None"
__credits__ = ["None"]
__license__ = "None"
__version__ = "1.0.0"
__maintainer__ = "Colleville Tanguy"
__email__ = "colleville.tanguy@gmail.coù"
__status__ = "Development"
########################################################Ma fenêtre Tkinter############################################

fen_princ = Tk()
fen_princ.title("Simulateur d'epidémie")
fen_princ.geometry("1000x1000")
xmax=700
ymax=700
## attention à faire gaffe au nom 
monCanvas = Canvas(fen_princ, width=xmax, height=ymax, bg='ivory', bd=0,)### la structure hôte de notre image
monCanvas.place(x=50,y=50)
#nb_malade_direct=Canvas(fen_princ, width=10, height=10, bg='white',bd=0)### notre petite image qui pop le nb infectés en directe

###########################################################Mes fonctions ###############################################
def norme(x1,y1,x2,y2):##norme euclidienne dans R²
    a=x2-x1
    b=y2-y1
    c=(a*a+b*b)**(0.5)
    return(c)
def temps_gueri(age):
    return(10*np.exp(age/100+1)+50)
def Probaguerir(age):
    m=22## age moyen 22 ans
    sigma=0.5##disperssion
    A=1/(sigma*((2*np.pi)**0.5))
    B=(age-m)**2
    C=2*sigma**2
    D=-B/C
    return(A*np.exp(D))
###########################################################Class Personne############################################
  
class personne():
    def __init__(self,r,state,x,y,v,theta,ID,Ti,immo):#définition d'une personne
        self._r=r##sa taille : le rayon du cercle
        self._x=x##sa position selon x 
        self._y=y##sa position selon y 
        self._v=v###la norme de sa vitesse
        self._theta=theta## l'angle de sa vitesse
        self._state=state## son etat malade ou pas
        self._age=rd.randint(0,80)
        self._Temps=Ti
        self._TG=temps_gueri(self._age)
        self._ID=ID
        self._immo=immo## 0 on bouge 1 on ne bouge pas 
        if self._state==0 :##0 =sain alors on le rpz par du bleu
            self._color="blue"
        elif self._state==1 :### 1 = malade on le fou en rouge
            self._color="red"
        if self._state==2:## mort noir
            self._color='black'
        if self._state==3:## green soigné
            self.color="green"
        self._graph=monCanvas.create_oval(self._x-r,self._y-r,self._x+r,self._y+r,fill=self._color)## on l'affiche
        #################défintions des gets#####################
    def Get_x(self):
        return(self._x)
    def Get_y(self):
        return(self._y)
    def Get_v(self):
        return(self._v)
    def Get_r(self):
        return(self._r)
    def Get_theta(self):
        return(self._theta)
    def Get_state(self):
        return(self._state)
    def Get_color(self):
        return(self._color)
    def Get_graph(self):
        return(self._graph)
    def Get_Temps(self):
        return(self._Temps)
    def Get_ID(self):
        return(self._ID)
    def Get_TG(self):
        return(self._TG)
    def Get_Immo(self):
        return(self._immo)
#######définitions des sets##################
    def Set_x(self,newx):
        self._x=newx
    def Set_y(self,newy):
        self._y=newy
    def Set_v(self,newv):
        self._v=newv
    def Set_r(self,newr):
        self._r=newr
    def Set_theta(self,newtheta):
        self._theta=newtheta
    def Set_state(self,newstate):
        self._state=newstate
        if newstate==1:
            self._color='red'
        elif newstate==2:
            self._color='black'
        elif newstate==3 :
            self._color='green'
        
    def Set_Temps(self,newt):
        self._Temps=newt
    
#############Méthode de personne######################
            
    def Creation(self):## permet de régenerer un cercle avec la bonne couleur lors d'un changement
        self._graph=monCanvas.create_oval(self._x-r,self._y-r,self._x+r,self._y+r,fill=self._color)
        
    def Motion(self):## fonction déplacement d'un obj
        if self.Get_Immo()==0 :
            if self.Get_x()>xmax-20 :   ### boudaries conditions
                self.Set_theta(rd.uniform(np.pi/2,3*np.pi/2))
                
            if self.Get_x()<20 :
                self.Set_theta(rd.uniform(-np.pi/2,np.pi/2))
               
            if self.Get_y()>ymax-20:
                
                self.Set_theta(rd.uniform(np.pi,2*np.pi))
            if self.Get_y()<20:
                self.Set_theta(rd.uniform(0,np.pi))
            '''
            if self.Get_x()>xmax-20 or self.Get_y()>ymax-20 or self.Get_y()<20 or self.Get_x()<20 :
                 self.Set_v(-self.Get_v())
                 #self.Set_theta(rd.uniform(0,np.pi))
            '''
            dx=self.Get_v()*np.cos(self.Get_theta())*deltat
            dy=self.Get_v()*np.sin(self.Get_theta())*deltat
            self.Set_x(self.Get_x()+dx)
            self.Set_y(self.Get_y()+dy)
            monCanvas.move(self.Get_graph(),dx,dy)
        else :
            pass
        
    def infection(self):### on infect infect un mec 
        self.Set_state(1)
        monCanvas.delete(self.Get_graph())###astuce pour change de couleur, on supprime la graph ave l'ancienne couleur
        self.Creation()###on redef son graph ici avec la nouvelle couleur du au changement de state
        self.Set_Temps(1)
        
    def Dead(self):
        monCanvas.delete(self.Get_graph())###astuce pour change de couleur, on supprime la graph ave l'ancienne couleur
    def Life(self):
            self.Set_state(3)
            monCanvas.delete(self.Get_graph())###astuce pour change de couleur, on supprime la graph ave l'ancienne couleur
            self.Creation()###on redef son graph ici avec la nouvelle couleur du au changement de state
 
        
            
#######################################################Class Population###########################################################     
class population():
    
    def __init__(self,N,v,r,borneinfx,bornesupx,borneinfy,bornesupy,nbinfecte,Tauximmo):## definition d'une population
        self._xmin=borneinfx## les bornes du canvas dans lequel on veut que la pop évolue
        self._ymin=borneinfy
        self._xmax=bornesupx
        self._ymax=bornesupy
        self._nbhab=N## son nombre d'habitant
        self._nbmalade=nbinfecte###son nb d'infecté
        self._nbsain=N-nbinfecte
        self._nbmort=0
        self._nbgueri=0
        self._count=0
        self._Pop=[]## la liste vide
        self._Tauximmo=Tauximmo
        self._Infecte=[]
        self._Sain=[]
        self._Gueri=[]
        self._DataS=[]
        self._DataI=[]
        self._DataG=[]
        self._DataM=[]
        self._Datapop=[]
        for i in range(0,N-nbinfecte):# on remplit/crée 'matériellement' la population
            cg=rd.randint(0,100)
            if cg<self._Tauximmo*100:
                self._Sain.append(personne(r,0,rd.randint(borneinfx+3*r,bornesupx-3*r),rd.randint(borneinfy+3*r,bornesupy-3*r),v,rd.uniform(0,2*np.pi),i,0,0))
            else :
                self._Sain.append(personne(r,0,rd.randint(borneinfx+3*r,bornesupx-3*r),rd.randint(borneinfy+3*r,bornesupy-3*r),v,rd.uniform(0,2*np.pi),i,0,1))
                
        for j in range(0,nbinfecte):
            cp=rd.randint(0,100)
            if cp<self._Tauximmo*100:
                self._Infecte.append(personne(r,1,rd.randint(borneinfx+3*r,bornesupx-3*r),rd.randint(borneinfy+3*r,bornesupy-3*r),v,rd.uniform(0,2*np.pi),j+self._nbhab-nbinfecte,1,0))
            else : 
                self._Infecte.append(personne(r,1,rd.randint(borneinfx+3*r,bornesupx-3*r),rd.randint(borneinfy+3*r,bornesupy-3*r),v,rd.uniform(0,2*np.pi),j+self._nbhab-nbinfecte,1,1))
        self._Pop=self._Sain+self._Gueri+self._Infecte

    def __del__(self):
        pass
    
    ######Mes gets##########
            
    def Get_Pop(self):
        return(self._Pop)
    def Get_nbhab(self):
        return(self._nbhab)
    def Get_nbsain(self):
        return(self._nbsain)
    def Get_nbgueri(self):
        return(self._nbgueri)
    def Get_nbmort(self):
        return(self._nbmort)
    def Get_ymin(self):
        return(self._ymin)
    def Get_ymax(self):
        return(self._ymax)
    def Get_xmin(self):
        return(self._xmin)
    def Get_xmax(self):
        return(self._xmax)
    def Get_nbmalade(self):
        return(self._nbmalade)
    def Get_count(self):
        return(self._count)
    def Get_Sain(self):
        return(self._Sain)
    def Get_Infecte(self):
        return(self._Infecte)
    def Get_Gueri(self):
        return(self._Gueri)
    
    ######Mes sets###########
    
    def Set_nbmalade(self,nbmadela):
        self._nbmalade=nbmadela
    def Set_count(self,newval):
        self._count=newval
    def Set_nbsain(self,newval):
        self._nbsain=newval
    def Set_nbgueri(self,newval):
        self._nbgueri=newval
    def Set_nbmort(self,newval):
        self._nbmort=newval
    ######mes fonctions#######
        
    def Add_Malade(self,indice):### ajoute un au nombre d'infeccté
        self._Infecte.append(self._Sain.pop(indice))
        self.Set_nbsain(len(self._Sain))
        self.Set_nbmalade(len(self._Infecte))
    def Add_Gueri(self,indice):
        self._Gueri.append(self._Infecte.pop(indice))
        self.Set_nbmalade(len(self._Infecte))
        self.Set_nbgueri(len(self._Gueri))
        
    def verifcontact(self,liste,k, taux):###vérification des contacts entre chaque individu de la population c=o(n!) :$
        ###taux est la proba de refiler la maladie
        if k==0 : ## si c'est la 1st time on prend la pop entière
            Pop=self.Get_Pop()
        else :## sinon on prend la liste donné en argument, ça permet d'avoir la récursivité bien d'où le [] quand j'appelle la fonction
            Pop=liste## comme lorsque j'appelle la fonction k=0 ma liste [] en argument n'est pas prise
        n=len(Pop)
        if n>1 :## tant qu'il a plus d'un élément dans ma liste
            xn=Pop[n-1].Get_x()## je recup la position du dernier élement 
            yn=Pop[n-1].Get_y()
            R=Pop[n-1].Get_r()## avec son rayon
            for i in range(0, len(Pop)-1): ## et je vérifie que les autres membres de la population ne lui rentre pas dedans
                xi=Pop[i].Get_x()## recup la position du mec i 
                yi=Pop[i].Get_y()
                if norme(xn,yn,xi,yi)<=2*R:### ici la condition de contact on pourrait add artificiellement la distance de transfert
                    if Pop[i].Get_state()==1 and Pop[n-1].Get_state()== 0   :## on fait la différence pour gérer les soins après ## utiliser les sous listes est plus malin --> plus fluidité
                        
                        a=rd.randint(0,100)## coté aléatoire du transfert
                        if a<taux*100:
                            Pop[n-1].infection()
                            kin=Pop[n-1].Get_ID()
                            p=0
                            for p in range(0,len(self._Sain)-1):
                                if self._Sain[p].Get_ID()==kin:  
                                    self.Add_Malade(p)## on contamine quelqu'un alors on update la liste des malade
                        else :
                            pass
                    if Pop[i].Get_state()==0 and Pop[n-1].Get_state()== 1:
                        b=rd.randint(0,100)
                        if b<taux*100:
                            Pop[i].infection()
                            
                            kinbis=Pop[i].Get_ID()
                            koko=0
                            for koko in range(0,len(self._Sain)-1):
                                if self._Sain[koko].Get_ID()==kinbis:
                                    self.Add_Malade(koko)## on contamine quelqu'un alors on incrémente le nb de malade
                        else :
                            pass
                else :
                     pass
            k+=1## très important pour la récursivité ça permet d'utiliser la liste qui est en argument 
            return(self.verifcontact(self.Get_Pop()[:(n-2)],k,taux))

    def Passage_d_etat(self):##PG = proba de guerir
        
        for h in range(0,len(self._Infecte)-6):## -2*N/100 deux je ne sais pas pourquoi pour 100 hab 6 pour 300 hab 
            self._Infecte[h].Set_Temps(self._Infecte[h].Get_Temps()+1)
            if self._Infecte[h].Get_Temps()>self._Infecte[h].Get_TG():## attention faut séparer mort et soin bb
                chance=rd.randint(0,100)
                if chance<Probaguerir(self._Infecte[h]._age)*100:
                    self._Infecte[h].Life()## on change son état mais on veut quand même la liste des gueri et des morts
                    ##ici les gens survivent donc on doit les retirer de infecte et les mettre dans gueri
                    mongueri=self._Infecte[h].Get_ID()
                    coco=0
                    for popa in range(0,len(self._Infecte)-1):
                        if self._Infecte[popa].Get_ID()==mongueri:
                            self.Add_Gueri(popa)
                else :
                    self._Infecte[h].Dead()###
                    monpetit=self._Infecte[h].Get_ID()
                    kij=0
                    for papo in range(0,len(self._Infecte)-1):
                        if self._Infecte[papo].Get_ID()==monpetit:
                            self.Set_nbmort(self._nbmort+1)
                            del self._Infecte[papo]##ici les gens meurent on doit donc les retirer de Infecte

    def ActuChif(self):
        self._DataS.append(self.Get_nbsain())                        
        self._DataI.append(self.Get_nbmalade())                             
        self._DataG.append(self.Get_nbgueri())
        self._DataM.append(self.Get_nbmort())    
        self._Datapop.append(self.Get_nbhab()-self.Get_nbmort())      
                    
r=10## rayon de notre population 
V=2
 ### vitesse de prop des habitants
#siinespi=0.1
deltat=1 ### echeelle de temps
N=100### taille de la population
k=0# un compteur à laisser nul pour le bon fonctionnement de verif contact en temps que méthode de population
Tau = 0.8 ### facteur de refilage de maladie
Tbouge=0.99### proportion de personne qui bouge
PopFra=population(N,V,r,0,xmax,0,ymax,3,Tbouge)## création d'une population
G=0.9### probaguerir

def modification():## main
    monCanvas.clipboard_clear()## nettoyage du canvas entre chaque iteration
    for i in range(0,len(PopFra.Get_Pop())):## on se promène dans la population hey mec fait le passer en méthode de pop
        PopFra.Get_Pop()[i].Motion()###on déplace chaque individu
    PopFra.verifcontact([],k,Tau)## et on vérifie les contact
    PopFra.ActuChif()
    PopFra.Passage_d_etat()
    PopFra.Set_count(PopFra.Get_count()+1)
    monCanvas.after(deltat,modification)## on actualise notre interface graphique
    return()

monCanvas.pack(padx=50,pady=50)
#nb_malade_direct.pack(padx=0,pady=0)
modification()#Affichage_infecte(),
fen_princ.mainloop()
print('le nb infecté',PopFra.Get_nbmalade())
lesmalades=PopFra._DataI
lessains=PopFra._DataS
lesmorts=PopFra._DataM
lesgueris=PopFra._DataG
envie=PopFra._Datapop

plt.figure()
plt.grid()
plt.title('évolution de la population')
plt.xlabel('temps')
plt.ylabel('nb habitant')
plt.plot(lesmalades,color='red',label='les infectés')
plt.plot(lessains,color='blue',label='les sains')
plt.plot(lesmorts,color='black',label='les morts')
plt.plot(lesgueris,color='green',label='les gueris')
plt.plot(envie,color='yellow',label='sanspb')
plt.legend()
plt.show()


