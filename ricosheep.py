from sys import setrecursionlimit
from time import time

from plateau import Plateau
from accueil import menu
import graphiques
import cfg
import fltk
import solveur
import sauvegarde
import son

setrecursionlimit(10**6)
DIRECTIONS = {'Up', 'Left', 'Right', 'Down'}

def jeu(plateau: Plateau):
    # créer la copie des moutons dans l'instance plateau

    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            plateau.draw()

            
            if plateau.isGagne():
                # graphiques.victory()
                print("C'est gagné !")
                # fltk.mise_a_jour()
                # fltk.attend_ev()

            ev = fltk.attend_ev()
            tev = fltk.type_ev(ev)
            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                touche = fltk.touche(ev)
                if touche in DIRECTIONS:
                    son.sound('Sheep')
                    plateau.deplace_moutons(touche, historique=True)

                if touche == "s":
                    start = time()
                    pos_tmp = solveur.tri_copy(plateau.troupeau)
                    chemin, _ = solveur.profondeur(plateau)
                    elapsed = time() - start
                    
                    if chemin == None:
                        print("Pas de solutions, chacal!")
                    else:
                        solveur.restore(plateau.troupeau, pos_tmp)
                        print(chemin)
                        print("Le solveur a bon? :", solveur.test(chemin, plateau, 0))
                        # print(chemin)
                        print(f"La longueur du chemin est de {len(chemin)},",
                              f"il a fallu {elapsed:.3f}s pour le déterminer.")

                elif touche == "r":
                    plateau.reset()
                elif touche == 'u':
                    plateau.undo()
                elif touche == 'Escape':
                    return
                elif touche == 'p':
                    print(cfg.carte_lst, plateau.historique, plateau.troupeau)
                    sauvegarde.save_write(cfg.carte_lst, plateau.historique, plateau.troupeau)
                """print('Historique :')
                pprint(plateau.historique)
                print('Troupeau :', plateau.troupeau)
                print()"""

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre,
                      'Ricosheep')
    son.initialisation()
    

    while True:
        son.song("Wait")
        plateau = menu()
        son.song("Otherside")
        jeu(plateau)