import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xml.etree.ElementTree as ET

# Renvoie la luminaisance d'une couleur c = [r, g, b]
def lum(c):
    return 0.2426 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


'''
color       couleur de la souris        (Cr, Cg, Cb)
love        attirance de la souris      (Sr, Sg, Sb)
prov_mouv   probabilités de mouvement   (Pg, Pt, Pd)
prov_suiv   probabilité de suivi        Ps
mouv_type   0=oblique, 1=angle droit    D
pos         position de départ          
dir         direction de départ         (north, south, east, west)
randStart   si True, pos et dir sont générés au hasard
'''
class Ant:

    def __init__(self, color=[0, 0, 0], love=[0, 0, 0], prob_mouv=[0.0, 0.9, 0.1], prob_suiv=0.5, mouv_type=1,
                 pos=(50, 50), dir='north', randStart=True):

        self.color = color
        self.love = love
        self.prob_mouv = prob_mouv
        self.prob_suiv = prob_suiv
        self.mouv_type = mouv_type

        if randStart:
            self.dir = np.random.choice(['north', 'south', 'east', 'west'])
            (self.x, self.y) = np.random.randint(0, h), np.random.randint(0, w)
        else:
            self.dir = dir
            (self.x, self.y) = pos[0], pos[1]

        data[self.x, self.y] = self.color

        print(f'New ant : color={self.color}, '
              f'love={self.love}, '
              f'dir={self.dir}, '
              f'pos={(self.x, self.y)}, '
              f'prob_mouv={self.prob_mouv}, '
              f'prob_suiv={self.prob_suiv}, '
              f'move_type={self.mouv_type}')

    # Renvoie les 3 mouvements possibles de la fourmi (en fonction de sa position, sa direction et de son type de déplacement)
    # Les "mouvements" sont codés sous le format suivant : [(posX, posY), 'direction']
    # Ainsi, position = mov[0] et direction = mov[1]
    # Note : renvoie toujours les 3 mouvements dans l'ordre : GAUCHE, TOUT DROIT, DROITE
    # TODO: faire ça plus intelligement ?
    def getMouvs(self):
        if self.mouv_type == 0:
            if self.dir == 'north':
                return [(self.x + 1, self.y - 1), 'west'], \
                       [(self.x + 1, self.y), 'north'], \
                       [(self.x + 1, self.y + 1), 'east'],
            elif self.dir == 'south':
                return [(self.x - 1, self.y - 1), 'west'], \
                       [(self.x - 1, self.y), 'south'], \
                       [(self.x - 1, self.y + 1), 'east']
            elif self.dir == 'east':
                return [(self.x + 1, self.y + 1), 'north'], \
                       [(self.x, self.y + 1), 'east'], \
                       [(self.x - 1, self.y + 1), 'south']
            elif self.dir == 'west':
                return [(self.x + 1, self.y - 1), 'north'], \
                       [(self.x, self.y - 1), 'west'], \
                       [(self.x - 1, self.y - 1), 'south']
        elif self.mouv_type == 1:
            if self.dir == 'north':
                return [(self.x, self.y - 1), 'west'], \
                       [(self.x + 1, self.y), 'north'], \
                       [(self.x, self.y + 1), 'east']
            elif self.dir == 'south':
                return [(self.x, self.y - 1), 'west'], \
                       [(self.x - 1, self.y), 'south'], \
                       [(self.x, self.y + 1), 'east']
            elif self.dir == 'east':
                return [(self.x + 1, self.y), 'north'], \
                       [(self.x, self.y + 1), 'east'], \
                       [(self.x - 1, self.y), 'south']
            elif self.dir == 'west':
                return [(self.x + 1, self.y), 'north'], \
                       [(self.x, self.y - 1), 'west'], \
                       [(self.x - 1, self.y), 'south']

    # Si la fourmi est attirée par une couleur dans son voisinage, renvoie la position de cette couleur, sinon renvoie False
    # TODO: diminuer le temps de calcul en appelant pas getMouvs() dans cette fonction?
    def isAttracted(self):
        # On récupère les mouvements possibles de la fourmi
        m1, m2, m3 = self.getMouvs()

        delta1 = delta2 = delta3 = 999

        # On calcule la différence de luminance entre la couleur détectée et la couleur d'attirance de la fourmi
        # Delta = | Lum(Sr, Sg, Sb) - Lum(Cr, Cg, Cb) |
        try:
            delta1 = abs(lum(self.love) - lum(data[m1[0]]))
            delta2 = abs(lum(self.love) - lum(data[m2[0]]))
            delta3 = abs(lum(self.love) - lum(data[m3[0]]))
        except IndexError:
            pass

        # Calcul du delta minimum et inférieur à 40 (seuil fixe)
        if delta1 < 40 and delta1 <= delta2 and delta1 <= delta3:
            return m1
        elif delta2 < 40 and delta2 <= delta1 and delta2 <= delta3:
            return m2
        elif delta3 < 40 and delta3 <= delta1 and delta3 <= delta2:
            return m3
        else:
            return False

    # Déplace la souris d'un pixel
    def move(self):
        # On commence par vérifier si la fourmi est attirée
        attracted = self.isAttracted()
        # Si oui, on génère un nombre aléatoire pour décider de si elle suit ou non la couleur
        if attracted:
            r = np.random.rand()
            if r <= self.prob_suiv:
                # Elle suit la couleur, on change sa position et sa direction
                (self.x, self.y) = attracted[0]
                self.dir = attracted[1]
        # Si non, on génère un nombre aléatoire pour décider de la direction qu'elle va emprunter
        else:
            r = np.random.choice(3, 1, p=self.prob_mouv) # Génère un nbr. entre 0 et 2 en respectant les poids 'prob_mouv'
            m1, m2, m3 = self.getMouvs()
            if r == 0:
                (self.x, self.y) = m1[0]
                self.dir = m1[1]
            elif r == 1:
                (self.x, self.y) = m2[0]
                self.dir = m2[1]
            elif r == 2:
                (self.x, self.y) = m3[0]
                self.dir = m3[1]

        # On modulo sa position par la taille du tableau (pour qu'elle passe d'un bord à l'autre)
        self.x = self.x % h
        self.y = self.y % w

        # Et enfin, la fourmi "laisse des phéromones" (= on applique sa couleur au tableau)
        data[self.x, self.y] = self.color

# Met à jour la figure
def updatefig(*args):
    for ant in ants:
        ant.move()
    im.set_array(data)
    return im,

# Génère une image en faisant bouger les fourmis autant de fois que le nombre d'itérations
# TODO: multithreader ça ?
def generatePicture(iterations):
    for i in range(iterations):
        for ant in ants:
            ant.move()
        if i % (iterations / 100) == 0:
            print(f'{(i / iterations) * 100:.0f}%')
    im.set_array(data)

def load_xml(path):
    global h
    global w
    global data

    tree = ET.parse(path)
    infos = tree.getroot()

    canvasData = infos[0]
    h = canvasData.attrib["height"]
    w = canvasData.attrib["width"]

    h, w = int(h), int(w)

    # Création de la toile avec comme couleur de fond = blanc (255, 255, 255)
    data = np.full((h, w, 3), 255)

    ants = []

    antsData = infos[1]
    for antData in antsData:
        mouv_type = int(antData.attrib["mouv_type"])
        prob_suiv = float(antData.attrib["prob_suiv"])
        color = [int(antData[0][0].text), int(antData[0][1].text), int(antData[0][2].text)]
        love = [int(antData[1][0].text), int(antData[1][1].text), int(antData[1][2].text)]
        prob_mouv = [float(antData[2][0].text), float(antData[2][1].text), float(antData[2][2].text)]

        ant = Ant(color=color, love=love, prob_mouv=prob_mouv, prob_suiv=prob_suiv, mouv_type=mouv_type)
        ants.append(ant)

    return ants

# ----- MAIN -----

fig = plt.figure()

# Dimensions de la toile et liste des fourmis
ants = load_xml("ants.xml")

# --- Génération des fourmis -----------------
'''for i in range(10):
    direction = np.random.choice(['north', 'south', 'east', 'west'])
    (posX, posY) = np.random.randint(0, h), np.random.randint(0, w)
    color = np.random.randint(50, 200, 3)
    love = np.random.randint(50, 200, 3)
    newAnt = Ant(color=color, love=love, dir=direction, pos=(posX, posY), prob_mouv=[0.5, 0.0, 0.5], prob_suiv=0.5)
    ants.append(newAnt)'''

'''ants.append(Ant(color=[233, 100, 106], love=[0, 0, 0], prob_mouv=[.5, .00, .5], prob_suiv=0.5))
ants.append(Ant(color=[244, 100, 97], love=[0, 0, 0], prob_mouv=[.01, .98, .01], prob_suiv=0.5))
ants.append(Ant(color=[231, 100, 81], love=[0, 0, 0], prob_mouv=[.01, .01, .98], prob_suiv=0.5))'''
# --------------------------------------------

im = plt.imshow(data, animated=True)
plt.axis([0, h, 0, w])  # <- pour afficher les axes
plt.axis('off')         # <- pour masquer les axes

# Au choix : animation en temps réel ou création de l'image finale (plus rapide)
#ani = animation.FuncAnimation(fig, updatefig, interval=20)
generatePicture(1000000)

plt.show()
