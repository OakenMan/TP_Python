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

        line = lines[0].replace(',', '.')
        data = line.split(';')
        lastDiff = float(data[4]) - float(data[2])  # Différence du cours entre la fin et le début de la minute

        for i in range(1, len(lines)):
            line = lines[i].replace(',', '.')
            data = line.split(';')

            newDiff = float(data[4]) - float(data[2])

            if (lastDiff >= 0 and newDiff >= 0) or (lastDiff < 0 and newDiff < 0):
                # Prédiction juste
                true += 1
            else:
                # Prédiction fausse
                false += 1

            lastDiff = newDiff

    accuracy = true / (true + false)
    print(f'true = {true}, false = {false}, total = {true + false}')
    print(f'Accuracy : {accuracy:.2f}')

# plotData()
# copieCarbone()
