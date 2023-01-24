from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pickle import load, dump
#Enregistrement
personne = {
    "identifiant" : str,
    "ntel" : str,
    "ville" : str,
    "genre" : str,
    "inscrit" : str
}
#Fonctions de verification
def verifPhone(ch:str) -> bool:
    if len(ch) == 8:
        i = 0
        valid = True
        while i < len(ch) and valid:
            if not(ch[i] >= "0" and ch[i] <= "9"):
                valid = False
            else:
                i = i + 1
        return valid
    else:
        return False

def verifId(ch:str) -> bool:
    if len(ch) >= 1 and len(ch) < 10:
        i = 0
        valid = True
        while i < len(ch) and valid:
            if not(ch[i] >= "0" and ch[i] <= "9" or ch[i].upper() >= "A" and ch[i].upper() <= "Z"):
                valid = False
            else:
                i = i + 1
        return valid
    else:
        return False
#Module ajouter    
def ajouter():
    identifiant = window.identifiant.text()
    telephone = window.numtel.text()
    if window.masculin.isChecked():
        genre = "Masculin"
    else:
        genre = "Feminin"
    ville = window.ville.currentText()
    inscrit = window.inscrit.isChecked()
    if identifiant == "" and telephone == "":
        QMessageBox.warning(window, "Error", "Vouillez Saisir Toute les Informations!")
    elif not(verifId(identifiant)):
        QMessageBox.warning(window, "Error", "Identifiant Invalide!")
    elif not(verifPhone(telephone)):
        QMessageBox.warning(window, "Error", "N° De Telephone Invalide!")
    else:
        F = open("Clients.dat", "ab")
        e = personne
        e["identifiant"] = identifiant
        e["ntel"] = telephone
        e["ville"] = ville
        e["genre"] = genre
        if inscrit:
            e["inscrit"] = "Inscrit"
        else:
            e["inscrit"] = "Non Inscrit"
        print(e)
        dump(e, F)
        F.close()
#Module affchance
def affchance():
    F = open("Chances.txt", "r")
    ligne = F.readline()
    while not(ligne == ""):
        window.chance_list.addItem(ligne[:len(ligne)-1])
        ligne = F.readline()
    F.close()
#Module affclient
def affclient():
    F = open("Clients.dat", "rb")
    FinFichier = False
    l = 0
    while not(FinFichier):
        try:
            e = load(F)
            l = l + 1
        except:
            FinFichier = True
    F.close()
    window.tableau.setRowCount(l)
    F = open("Clients.dat", "rb")
    for i in range(l):
        e = load(F)
        window.tableau.setItem(i, 0, QTableWidgetItem(e["identifiant"]))
        window.tableau.setItem(i, 1, QTableWidgetItem(e["ntel"]))
        window.tableau.setItem(i, 3, QTableWidgetItem(e["genre"]))
        window.tableau.setItem(i, 2, QTableWidgetItem(e["ville"]))
        window.tableau.setItem(i, 4, QTableWidgetItem(e["inscrit"]))
    F.close()
#Module affgagnant
def affgagnant():
    F2 = open("Clients.dat", "rb")
    FinFichier = False
    window.gagne_list.addItem("Les Clients Gagnants Sont :")
    while not(FinFichier):
        try:
            e = load(F2)
            num1 = e["ntel"]
            s1 = 0
            for i in range(len(num1)):
                s1 = s1 + int(num1[i])
            s2 = 0
            num2 = str(s1)
            for i in range(len(num2)):
                s2 = s2 + int(num2[i])
            F1 = open("Chances.txt", "r")
            ligne = F1.readline()
            trouve = False
            while not(ligne == "") and not(trouve):
                ligne = ligne[:len(ligne)-1]
                if str(s2) == ligne:
                    trouve = True
                ligne = F1.readline()
            F1.close()
            if trouve:
                ch = "Identifiant : " + e["identifiant"] + "-" + "N°Telephone : " + num1
                window.gagne_list.addItem(ch)
        except:
            FinFichier = True
    F2.close()
#Programme Principale
app = QApplication([])
window = loadUi("window.ui")
window.ajouter.clicked.connect(ajouter)
window.affiche_chance.clicked.connect(affchance)
window.affiche_client.clicked.connect(affclient)
window.affiche_gagnant.clicked.connect(affgagnant)
window.show()
app.exec_()