import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
import random

# 1. Générer des nombres aléatoires
random.seed()
list = [random.randint(0, 9) for i in range(100)]

print(list)

# 2-3-4. Afficher ces données
fig, axis = plt.subplots(2, 2)

fig.set_figheight(10)
fig.set_figwidth(10)

axis[0, 0].plot(list)
axis[0, 0].set_title("Defaut")

axis[0, 1].plot(list, linestyle='None', marker='.', color='r')
axis[0, 1].legend(['Point'])
axis[0, 1].set_title("Avec légende")

axis[1, 0].plot(list, marker='+', color='g', linewidth=1)
axis[1, 0].set_xlabel("Axe 1")
axis[1, 0].set_ylabel("Axe 2")
axis[1, 0].set_title("Avec noms d'axes")

axis[1, 1].plot(list, linestyle='dashed', color='k')
axis[1, 1].arrow(0, 5, 50, 0, linewidth=3, head_width=2, head_length=10)
axis[1, 1].set_title("Avec flèche")

plt.show()

# 5. Histogramme et camembert
plt.hist(list)
plt.title("Histogramme")
plt.xlabel("Chiffre")
plt.ylabel("Fréquence")
plt.xticks(range(10))
plt.show()

count = []
for i in range(10):
    count.append(list.count(i))
plt.pie(count, labels=range(10))
plt.title("Camembert")
plt.show()

# 6. Mesh
fig = plt.figure()
ax = fig.gca(projection='3d')

# On créé les données : on veut afficher z = cos(sqrt(x^2 + y^2))
X = np.arange(-10, 10, 0.25)
Y = np.arange(-10, 10, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.cos(np.sqrt(X**2 + Y**2))

# On affiche la surface            cmap = gradient de couleur utilisé pour l'affichage
surface = ax.plot_surface(X, Y, Z, cmap=cm.hot, linewidth=0, antialiased=False)
ax.set_zlim(-1.05, 1.05)

# Légende de la cmap
fig.colorbar(surface, shrink=0.7, aspect=10)

plt.show()

