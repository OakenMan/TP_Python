import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Renvoie la luminaisance d'une couleur c = [r, g, b]
def lum(c):
    return 0.2426 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


'''
color       couleur de la souris        (Cr, Cg, Cb)
love        attirance de la souris      (Sr, Sg, Sb)
prov_mouv   probabilités de mouvement   (Pg, Pt, Pd)
prov_suiv   probabilité de suivi        Ps
mouv_type   0=oblique, 1=angle droit    D
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

    # Renvoie les 3 mouvements possibles de la fourmi (en fonction de sa direction et de son type de déplacement)
    # TODO: faire ça plus intelligement ?
    def getMouvs(self):
        if self.mouv_type == 0:
            if self.dir == 'north':
                return [(self.x + 1, self.y - 1), 'west'], [(self.x + 1, self.y), 'north'], [(self.x + 1, self.y + 1),
                                                                                             'east'],
            elif self.dir == 'south':
                return [(self.x - 1, self.y - 1), 'west'], [(self.x - 1, self.y), 'south'], [(self.x - 1, self.y + 1),
                                                                                             'east']
            elif self.dir == 'east':
                return [(self.x + 1, self.y + 1), 'north'], [(self.x, self.y + 1), 'east'], [(self.x - 1, self.y + 1),
                                                                                             'south']
            elif self.dir == 'west':
                return [(self.x + 1, self.y - 1), 'north'], [(self.x, self.y - 1), 'west'], [(self.x - 1, self.y - 1),
                                                                                             'south']
        elif self.mouv_type == 1:
            if self.dir == 'north':
                return [(self.x, self.y - 1), 'west'], [(self.x + 1, self.y), 'north'], [(self.x, self.y + 1), 'east']
            elif self.dir == 'south':
                return [(self.x, self.y - 1), 'west'], [(self.x - 1, self.y), 'south'], [(self.x, self.y + 1), 'east']
            elif self.dir == 'east':
                return [(self.x + 1, self.y), 'north'], [(self.x, self.y + 1), 'east'], [(self.x - 1, self.y), 'south']
            elif self.dir == 'west':
                return [(self.x + 1, self.y), 'north'], [(self.x, self.y - 1), 'west'], [(self.x - 1, self.y), 'south']

    # Si la fourmi est attirée par une couleur voisine, renvoie sa position, sinon envoie false
    def isAttracted(self):
        m1, m2, m3 = self.getMouvs()
        lum1 = lum2 = lum3 = 999

        try:
            lum1 = abs(lum(self.love) - lum(data[m1[0]]))
            lum2 = abs(lum(self.love) - lum(data[m2[0]]))
            lum3 = abs(lum(self.love) - lum(data[m3[0]]))
        except IndexError:
            pass

        if lum1 < 40 and lum1 <= lum2 and lum1 <= lum3:
            return m1
        elif lum2 < 40 and lum2 <= lum1 and lum2 <= lum3:
            return m2
        elif lum3 < 40 and lum3 <= lum1 and lum3 <= lum2:
            return m3
        else:
            return False

    def move(self):
        attracted = self.isAttracted()
        if attracted:
            r = np.random.rand()
            if r <= self.prob_suiv:
                # Il suit la couleur
                (self.x, self.y) = attracted[0]
                self.dir = attracted[1]
                return
        r = np.random.choice(3, 1, p=self.prob_mouv)
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

        self.x = self.x % h
        self.y = self.y % w

        data[self.x, self.y] = self.color


def updatefig(*args):
    for ant in ants:
        ant.move()
    im.set_array(data)
    return im,


def generatePicture(iterations):
    for i in range(iterations):
        for ant in ants:
            ant.move()
        if i % (iterations / 100) == 0:
            print(f'{(i / iterations) * 100:.0f}%')
    im.set_array(data)


# ----- MAIN -----

fig = plt.figure()

h = 500
w = 500

data = np.full((h, w, 3), 255)

ants = []

'''for i in range(5):
    direction = np.random.choice(['north', 'south', 'east', 'west'])
    (posX, posY) = np.random.randint(0, h), np.random.randint(0, w)
    color = np.random.randint(50, 200, 3)
    love = np.random.randint(50, 200, 3)
    newAnt = Ant(color=color, love=love, dir=direction, pos=(posX, posY), prob_mouv=[0.5, 0.0, 0.5], prob_suiv=0.5)
    ants.append(newAnt)'''

ants.append(Ant(color=[38, 70, 83], love=[42, 157, 143], prob_mouv=[0.8, 0.1, 0.1], prob_suiv=0.9))
ants.append(Ant(color=[42, 157, 143], love=[233, 196, 106], prob_mouv=[0.8, 0.1, 0.1], prob_suiv=0.9))
ants.append(Ant(color=[233, 0, 106], love=[0, 0, 0], prob_mouv=[.01, 0.98, .01], prob_suiv=0.5))
ants.append(Ant(color=[244, 0, 97], love=[0, 0, 0], prob_mouv=[.01, 0.98, .01], prob_suiv=0.5))
ants.append(Ant(color=[231, 0, 81], love=[0, 0, 0], prob_mouv=[.01, 0.98, .01], prob_suiv=0.5))


im = plt.imshow(data, animated=True)
plt.axis([0, h, 0, w])
plt.axis('off')

#ani = animation.FuncAnimation(fig, updatefig, interval=20)
generatePicture(500000)

plt.show()
