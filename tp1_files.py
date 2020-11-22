print("Bonjour tout le monde!")

print("1. Choisir un nom de fichier :")

filename = input()

try:
    file = open(filename, 'r')
except FileNotFoundError:
    print("Error: No such file or directory : {0}".format(filename))
except IsADirectoryError:
    print("Error: {0} is a directory".format(filename))
else:
    lines = file.readlines()
    print(f'Contenu de {filename}:')
    for line in lines:
        print(line[:-1])
    # On clear tout en l'ouvrant en écriture
    open(filename, 'w')
finally:
    exit()

