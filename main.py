# remarque : erreur => impossible de modifier l'une des valeurs d'un tuple ???? -> transformation des tuples en list !
# Test avec dycotomie
########################################################################################################################
# UTF-8
# HAMADI Mohand & CORREC Pierre
# Realise dans le cadre du projet d ISN au Baccalaureat 2018-2019
# Objectif: Generer la page d un article d un site web facilement via une interface graphique !
#           Cadre d'utilisation: Generer la page d un article sur un site web d actualite par exemple ...
# Update à faire /!\ :
#      Ajouter un bouton supprimer afin de supprimer le paragraphe
#      Ajouter la gestion des couleurs etc...

# Imports
import pygame
import os
from math import *

# Initalisation des modules
pygame.init()
pygame.font.init()

# Couleurs
CouleurPolice=pygame.Color('black')
CouleurArrierePlan=pygame.Color('white')

# Couleurs du champ
CPolice=(0,0,0) # noir - nom de variable a conserver
CFond=(192,192,192) # gris - nom de variable a conserver
CFondActif=(255,255,255) # blanc - nom de variable a conserver


# Police d ecriture
Police=pygame.font.SysFont("Avenir",32) # nom de variable a conserver
PoliceXL=pygame.font.SysFont("Avenir",52)


# Variable
listParagraphes =[]
marge = 80
attribut = {
    (0,0,0) : "noir",
    (255,0,0) : "rouge",
    (0,255,0) : "vert",
    (0,0,255) : "bleu"
}

lettreCoul = { #permet de donner la couleur en fonction du msg du boutton
    "B":(0,0,255),
    "V": (0,255,0),
    "R":(255,0,0)
}

lettreForme = { # rang du parametre dans "set" -> Boitetexte
    "I":1,
    "G":2,
    "S":3
}

# Creation Fenetre
Fenetre = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
Fenetre.fill(CouleurArrierePlan)


# Classes et fonctions Principales
class BoiteTexte:
    """BoiteTexte((int, int), (int, int)) -> BoiteTexte
    Attributs :
    - pos (abscisse, ordonnee du coin superieur gauche) : (int, int)
        (0,0) par defaut
    - dim (largeur, hauteur du cadre) : (int, int)
        (100,20) par defaut
    - actif (possibilite d ecrire ou non) : bool - valeur initiale : False
    - msg (contenu par default) : str - valeur initiale de txt et valeur de reference pour les textes.
    - txt (contenu) : str - valeur initiale : msg
    """
    def __init__(self,pos=(10,10),dim=(500,40), msg="Ecrivez ici"):
        self.dimFixe = [dim[0], dim[1]]
        self.posFixe = [pos[0], pos[1]]
        
        self.pos = [pos[0], pos[1]]
        self.dim = [dim[0], dim[1]]
        
        self.actif=False

        self.msg = msg
        self.txt= msg

        self.set = [
            (0,0,0),
            False, # Italique
            False, # Gras
            False, # Souligne 
        ]

        self.specBut = [
            Bouton(
            pos = (self.pos[0], self.pos[1]+self.dim[1]+5),
            msg = "",
            couleur = self.set[0]
            ),
        
            Bouton(
            pos = (self.pos[0] +55, self.pos[1]+self.dim[1]+5),
            msg = "I",
            couleur = (0,255,0)
            ),

            Bouton(
            pos = (self.pos[0] + 110, self.pos[1]+self.dim[1]+5),
            msg = "G",
            couleur = (0,255,0)
            ),

            Bouton(
            pos = (self.pos[0] + 165, self.pos[1]+self.dim[1]+5),
            msg = "S",
            couleur = (0,255,0)
            ),
        ]

    def __contains__(self,pos):
        """(int, int) in BoiteTexte -> bool
        Appartenance d un point au rectangle ferme BoiteTexte"""
        # Permet de donner une contenance a l objet
        # Il devient comme une liste de point
        # Ainsi on peut le parcourir comme on le ferai avec une liste
        xmin=self.pos[0]
        xmax=self.pos[0]+self.dim[0]
        ymin=self.pos[1]
        ymax=self.pos[1]+self.dim[1]
        xpt=pos[0]
        ypt=pos[1]
        return (xpt>=xmin and xpt<=xmax and ypt>=ymin and ypt<=ymax)

    def activer(self):
        """Rend la saisie possible dans BoiteTexte et vide le contenu.
        BoiteTexte.actif prend la valeur True
        Actualise l affichage"""
        if self.txt == self.msg: self.txt="" #Efface juste le message de saisie...
        self.actif=True
        self.afficher()

    def desactiver(self):
        """Rend la saisie impossible dans BoiteTexte.
        BoiteTexte.actif prend la valeur False
        Actualise l affichage"""
        self.actif=False
        if self.txt == "":self.txt=self.msg #Permet de remettre l instruction si la zone de saisir est vide...
        self.afficher()

    def corrigeLigne(self):
        Texte=Police.render(self.txt, True, CPolice) # Rendu du texte
        self.lignes = []

        if Texte.get_width() < self.dim[0]: self.lignes.append(Ligne(self.txt))
        else:
            rangD = 0 # Ne doit pas etre reinitialise
            verif = "" # Initialisation, permet de verifier si tout le texte est coupe
            while verif != self.txt:
                rangF = len(self.txt)-1 # doit etre reinitialiser a chaque tour
                while Texte.get_width() > self.dim[0]:
                    rangF -= 1
                    Texte = Police.render(self.txt[rangD:rangF], True, CPolice)
                self.lignes.append(self.txt[rangD:rangF])
                verif += self.txt[rangD:rangF]
                rangD = rangF


    def afficher(self):
        """Actualise l affichage du champ texte"""

        #self.corrigeLigne()
        
        #self.dim[1] = self.dim[1]*len(self.lignes)
        if self.actif: CoulAP=CFondActif # Def couleur de fond
        else: CoulAP=CFond

        bordureRectPrec = (self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        pygame.draw.rect(Fenetre, CouleurArrierePlan, bordureRectPrec,0)
        
        Texte=Police.render(self.txt, True, CPolice)

        self.dim[0] = Texte.get_width()+20

        bordureRect = (self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        
        pygame.draw.rect(Fenetre, CoulAP, bordureRect,0) # Dessine le fond
        pygame.draw.rect(Fenetre, CPolice, bordureRect, 1) # Dessine les bords

        for but in range(len(self.specBut)):
            if but != 0:
                if self.set[but] == True:
                    self.specBut[but].couleur = (0,255,0)
                    self.specBut[but].afficher()
                else:
                    self.specBut[but].couleur = CFond
                    self.specBut[but].afficher()
            else:
                self.specBut[but].couleur = self.set[0]
                self.specBut[but].afficher()

        #for compteur in range(0, len(self.lignes)):
        #    position = (self.pos[0], self.pos[1]+compteur*self.dimFixe[1])
        #    self.lignes[compteur].afficher(position)

        Fenetre.blit(Texte, (self.pos[0], self.pos[1]))
          
        pygame.display.flip() #Actualise

    def saisir(self):
        """BoiteTexte.saisir() -> bool
        Met a jour BoiteTexte.txt
        Actualise l affichage"""
        Caracteres=[chr(k) for k in range(32,254+1)] # Genere la liste des caracteres pouvant etre saisie, 34-> Espace, 254-> Dernier caractere (ASCII Extend)
        self.activer()
        while True:
            for entree in pygame.event.get():
                #Actions Souris
                if entree.type==pygame.MOUSEBUTTONDOWN: 
                    if pygame.mouse.get_pressed()[0]==1: 
                        
                        if not pygame.mouse.get_pos() in self: # Clic en dehors -> Desactivation
                            self.desactiver()
                            return True

                #Actions appuis Clavier
                if entree.type==pygame.KEYDOWN:
                    
                    if entree.unicode in Caracteres: # Permet de saisir les caracteres
                        self.txt+=entree.unicode
                        self.afficher()
                    
                    if entree.key==pygame.K_RETURN: # Appuie sur ENTREE -> Desactivation
                        self.desactiver()
                        return True
                    
                    if entree.key==pygame.K_ESCAPE:
                        self.desactiver()
                        return True
                    
                    if entree.key==pygame.K_BACKSPACE: # Permet d effacer lors de l appuie sur "retour"
                        self.txt=self.txt[:len(self.txt)-1]
                        self.afficher() # Actualise


class Ligne:
    def __init__(self, text):
        self.txt = text
    
    def afficher(self, pos):
        Texte = Police.render(self.txt, True, CPolice)
        Fenetre.blit(Texte, pos) #On colle


class Bouton:
    """
        Cette classe va nous permettre de definir les boutons et simplifier leurs implementantion.
         - pos (int,int) -> coordonnees (abscisse, origine) du point d'origine
         - dim (int,int) -> dimensions du bouton (largueur, hauteur)
         - msg (txt) -> Message afficher dans le cadre du bouton
    """
    def __init__(self,pos=(0,0),dim=(40,20),msg="Cliquez", couleur = CFond):
        self.pos=pos
        self.dim=dim
        self.msg=msg
        self.couleur = couleur
        self.ParametresBte = (self.pos[0], self.pos[1], self.dim[0]+10, self.dim[1]) # Rect de la boite, avec marge sur la largueur

    def __contains__(self,pos):
        """(int, int) in BoiteTexte -> bool
        Appartenance d un point au rectangle ferme BoiteTexte"""
        # Permet de donner une contenance a l objet
        # Il devient comme une liste de point
        # Ainsi on peut le parcourir comme on le ferai avec une liste
        xmin=self.pos[0]
        xmax=self.pos[0]+self.dim[0]
        ymin=self.pos[1]
        ymax=self.pos[1]+self.dim[1]
        xpt=pos[0]
        ypt=pos[1]
        return (xpt>=xmin and xpt<=xmax and ypt>=ymin and ypt<=ymax)

    def afficher(self):
        """Actualise l affichage du champ texte"""

        Texte=Police.render(self.msg,True,CPolice) # Rendu du texte

        Rectangle=pygame.draw.rect(Fenetre, self.couleur, self.ParametresBte,0) # Dessine le fond
        Bords=pygame.draw.rect(Fenetre, CPolice, self.ParametresBte, 1) # Dessine les bords

        HTexte=Texte.get_rect()[3] #Hauteur du texte

        PosTexte=(self.pos[0]+5, self.pos[1]+int((self.dim[1]-HTexte)/2)) # x-> on laisse une marge de 5px depuis le bord gauche /// y-> hauteur de la boite - (hauteur du texte)/2 --> Permet de centrer le texte au centre de la boite

        Fenetre.blit(Texte, PosTexte) #On colle
        pygame.display.flip() #Actualise


def Enregistrer(codeHtml):
    urlFichier = 'ressources/pages/p'
    compteur = 1
    if os.path.exists(urlFichier):
        while os.path.exists(urlFichier+str(compteur)):
            compteur += 1
    urlFichier = urlFichier + str(compteur)+".html"
    with open(urlFichier, "w") as file:
        file.write(codeHtml)
    return True


def GenStyle(listParagraphes, typeC):
    paragraphesHtml = ""
    for paragraphe in listParagraphes:
        paragraphesHtml += '<'+typeC
        paragraphesHtml += ' class = "'+str(attribut[paragraphe.set[0]])
        if paragraphe.set[1] == True: paragraphesHtml += " italique"
        if paragraphe.set[2] == True: paragraphesHtml += " gras"
        if paragraphe.set[3] == True: paragraphesHtml += " souligne"
        paragraphesHtml += '">'+paragraphe.txt+'</'+typeC+'>'
    return paragraphesHtml


def Ecriture(titre,listParagraphes):
    enteteHtml = '<!DOCTYPE html><html lang="fr"><head><title>'+titre.txt+'</title><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="attributs.css"></head>' #Utilisation des guillemets simples pour eviter d echapper les guillemets doubles utilise dans le language html
    
    paragraphesHtml = GenStyle(listParagraphes, "p")
    
    titreHtml = GenStyle([titre], "h1") # On passe une list de 1 objet sinon la boucle for parcours les lettres
    
    codeHtml = enteteHtml+'<body>'+'<header>'+titreHtml+'</header>'+'<article>'+paragraphesHtml+'</article></body></html>'
    Enregistrer(codeHtml)
    return True


def FenetrePrincipale():
    #Def element
    Titre = BoiteTexte(pos=(280, 10),msg="Saisissez le titre de la page !")
    Titre.afficher()
    
    for but in coulBoutton:
        but.afficher()
    for but in styleBoutton:
        but.afficher()
    

    AjtParagraphe=Bouton((10,600),(250,30),"Ajouter un paragraphe")
    AjtParagraphe.afficher()

    CreerPage = Bouton((10,650),(250,30),"Créer une page !")
    CreerPage.afficher()

    boiteActif = Titre

    #Boucle Principale
    continuer = True
    while continuer:
        for event in pygame.event.get():

            if event.type==pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]==1:

                    # Va contenir tout les boutons et les boites
                    if pygame.mouse.get_pos() in Titre: # --> Voir classe BoiteTexte -> __contains__
                        boiteActif = Titre
                        Titre.saisir()

                    if pygame.mouse.get_pos() in AjtParagraphe:
                        if listParagraphes == []:
                            if Titre.txt != Titre.msg:
                                listParagraphes.append(BoiteTexte(pos=(280,Titre.pos[1]+Titre.dim[1]+marge)))

                        else:
                            boitePreced = listParagraphes[len(listParagraphes)-1]
                            if boitePreced.txt != boitePreced.msg:
                                nellePos = (boitePreced.pos[0], (boitePreced.pos[1]+boitePreced.dim[1]+marge))
                                listParagraphes.append(BoiteTexte(pos=nellePos))
     
                        for par in listParagraphes:
                            par.afficher()

                    for boiteP in listParagraphes:
                        if pygame.mouse.get_pos() in boiteP:
                            boiteActif = boiteP
                            boiteP.saisir()
                           
                    if pygame.mouse.get_pos() in CreerPage:
                        ecrit = Ecriture(Titre, listParagraphes)
                        if ecrit == True:
                            pygame.quit()
                            quit()

                    for butCoul in  coulBoutton:
                        if pygame.mouse.get_pos() in butCoul:
                            boiteActif.set[0] = lettreCoul[butCoul.msg]
                            boiteActif.specBut[0].afficher()
                            pygame.display.flip()
                    
                    for butForme in styleBoutton:
                        if pygame.mouse.get_pos() in butForme:
                            precEtat = boiteActif.set[lettreForme[butForme.msg]]
                            if precEtat == True:
                                boiteActif.set[lettreForme[butForme.msg]] = False
                            elif precEtat == False:
                                boiteActif.set[lettreForme[butForme.msg]] = True
                        boiteActif.afficher()
                        pygame.display.flip()
                    
            if event.type==pygame.QUIT:
                continuer=False


########## Var supplementaires ....
coulBoutton = [
    Bouton(
        pos = (10,200),
        msg = "B",
        couleur=(0,0,255)
        ),
     Bouton(
        pos = (10,250),
        msg = "R",
        couleur=(255,0,0)
        ),
    Bouton(
        pos = (10,300),
        msg = "V",
        couleur=(0,255,0)
        )
    ]

styleBoutton = [

    Bouton(
        pos = (10,350),
        msg = "S",
        ),
            
    Bouton(
        pos = (10,400),
        msg = "G",
        ),

    Bouton(
        pos = (10,450),
        msg = "I",
        )

    ]
###########





FenetrePrincipale()
