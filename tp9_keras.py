import matplotlib.pyplot as plt


def plotData():
    with open("/home/tom/Téléchargements/TP Python/ForexData/data_2019.csv", 'r') as file:
        lines = file.readlines()
        closes = []
        for i in range(10000):
            line = lines[i]
            data = line.split(';')
            closes.append(data[4])
        plt.plot(closes)
        plt.show()


def copieCarbone():
    true = 0
    false = 0

    with open("/home/tom/Téléchargements/TP Python/ForexData/data_2019.csv", 'r') as file:
        lines = file.readlines()

        # On récupère la différence du cours de l'euro sur la première ligne
        line = lines[0].replace(',', '.')   # On remplace les , par des . pour que python arrive à lire les nombres
        data = line.split(';')
        lastDiff = float(data[4]) - float(data[2])  # Différence du cours entre la fin et le début de la minute

        # Puis on fait des prédictions sur chaque minute
        for i in range(1, len(lines)):
            line = lines[i].replace(',', '.')
            data = line.split(';')

            newDiff = float(data[4]) - float(data[2])

            # Si la nouvelle et l'ancienne différence sont du même signe...
            if (lastDiff >= 0 and newDiff >= 0) or (lastDiff < 0 and newDiff < 0):
                true += 1   # Prédiction juste
            # Sinon...
            else:
                false += 1  # Prédiction fausse

            lastDiff = newDiff

    accuracy = true / (true + false)
    print(f'true = {true}, false = {false}, total = {true + false}')
    print(f'Accuracy : {accuracy:.2f}')

#plotData()
copieCarbone()
