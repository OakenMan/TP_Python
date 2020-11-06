import numpy as np
from scipy.optimize import curve_fit
from scipy import ndimage
from scipy import linalg
from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt

# ---------- NUMPY ----------

# Paramètres d'un tableau Numpy
arr = np.random.rand(4, 3, 2)
print(f'ndim = {arr.ndim}')
print(f'shape = {arr.shape}')
print(f'size = {arr.size}')
print(f'dtype = {arr.dtype}')
print(f'itemsize = {arr.itemsize}')
print(f'data = {arr.data}')  # affiche l'adresse mémoire du tableau
print(arr)  # affiche le contenu du tableau

# arange et reshape
A = np.arange(0, 9).reshape(3, 3)
B = np.arange(2, 11).reshape(3, 3)
print(f'A = \n{A}')
print(f'B = \n{B}')

# Produit scalaire et matriciel
product = A * B
dotproduct = np.dot(A, B)
print(f'A * B = \n{product}')
print(f'A . B = \n{dotproduct}')

# Transposée
transposed = A.transpose()
print(f'A^T = \n{transposed}')

# Déterminant
det = np.linalg.det(A)
print(f'det(A) = \n{det}')

# Inverse
inv = np.linalg.inv(product)
print(f'inv(A) = \n{inv}')

# Résolution de système linéaire
a = np.array([[2, 3, 3, 1],
              [-4, -6, 3, 2],
              [-1, 1, 1, 1],
              [-2, -1, 1, 1]])
b = np.array([15, 3, 5, 1])
x = np.linalg.solve(a, b)
print(f'x = \n{x}')

# Valeurs et vecteurs propres
val_propres = np.linalg.eig(A)[0]
vect_propres = np.linalg.eig(A)[1]
print(f'valeurs propres(A) = {val_propres}')
print(f'vecteurs propres(A) = {vect_propres}')

# ---------- SCIPY ----------

# Fonction utilisée pour modéliser les données
def func(x, a, b, c):
    return a / (1.0 + b * np.exp(c * -x))

# Génération des données
x = np.linspace(-10, 10, 100)
y = func(x, 20, 10, 1)
# On ajoute du bruit
noise = 0.9 * np.random.normal(size=x.size)
y_noise = y + noise

# 'init_vals' peut être configuré si on peut estimer les params du modèle
# afin d'aider 'curve_fit' à converger vers des paramètres optimaux
# (ici même avec les valeurs par défaut (1 partout), curve_fit converge quand même
init_vals = [1, 1, 1]
opti_vals, covar = curve_fit(func, x, y_noise, p0=init_vals)
print(f'Best params = {opti_vals}')
y_fit = func(x, opti_vals[0], opti_vals[1], opti_vals[2])

# On plot les 3 courbes
plt.plot(x, y, label='y')
plt.scatter(x, y_noise, label='y_noise', s=3)
plt.plot(x, y_fit, label='y_fit')

plt.legend()
plt.grid()
plt.show()

# ---------- Lecture/Manipulation d'images ----------
# (pas besoin de Scipy pour juste ouvrir et redimensionner une image)
img = io.imread("image.jpg")
plt.imshow(img)
plt.show()

resized = resize(img, (100, 100))
plt.imshow(resized)
plt.show()

# ---------- Autres exemples Scipy ----------

# Calculer un déterminant
A = np.array([[1, 2], [3, 4]])
det = linalg.det(A)
print(f'det(A) = {det}')

# Calculer l'inverse d'une matrice
inv = linalg.inv(A)
print(f'inv(A) = {inv}')

# Calculer des normes
norm = linalg.norm(A)
print(f'norm(A) = {norm}')

# Ajout de flou sur une image
blurred = ndimage.gaussian_filter(img, sigma=10)
plt.imshow(blurred)
plt.show()

# Détection des bords
shapes = io.imread("shapes.png")
sx = ndimage.sobel(shapes, axis=0, mode='constant')
sy = ndimage.sobel(shapes, axis=1, mode='constant')
edges = sx + sy
plt.imshow(edges)
plt.show()
