import numpy as np

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

from keras.models import Sequential
from keras.layers import Conv1D, Dropout, MaxPooling1D, Flatten, Dense
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping

# Renvoie les données sous la forme suivante
# X.shape = (end-start-last_mn, last_mn, 4)
# Y.shape = (end-start-last_mn, last_mn)
# X[n][0] = [open, high, low, close]
# Y[n]    = 1 si augmentation, 0 si diminution
def prepare_data(path, start, end, last_mn=120):
    X = []
    Y = []

    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(start, end-last_mn):
            x = []
            for j in range(i, i+last_mn):
                data = lines[j].replace(',', '.').split(';')
                xj = [float(data[1]), float(data[2]), float(data[3]), float(data[4])]
                x.append(xj)
            if float(lines[i+last_mn].replace(',', '.').split(';')[4]) - float(lines[i+last_mn-1].replace(',', '.').split(';')[4]) >= 0:
                y = 1
            else:
                y = 0
            X.append(x)
            Y.append(y)

    X = np.asarray(X)
    Y = np.asarray(Y)
    return X, Y

def load_dataset():
    trainX, trainY = prepare_data("/home/tom/Téléchargements/TP Python/ForexData/data_2019.csv", 0, 100000)
    testX, testY = prepare_data("/home/tom/Téléchargements/TP Python/ForexData/data_2019.csv", 100000, 150000)

    print(f'nb augmentation : {np.count_nonzero(trainY == 1)}')
    print(f'nb diminutions : {np.count_nonzero(trainY == 0)}')

    trainY = to_categorical(trainY)
    testY = to_categorical(testY)

    print(f'Dataset chargé!')
    print(f'trainX: {trainX.shape}, trainY: {trainY.shape}, testX: {testX.shape}, testY: {testY.shape}')

    return trainX, trainY, testX, testY

# ---------------------------------------
trainX, trainY, testX, testY = load_dataset()

timesteps = trainX.shape[1]
features = trainX.shape[2]
outputs = trainY.shape[1]

print(f'timesteps = {timesteps}')
print(f'features = {features}')
print(f'outputs = {outputs}')

model = Sequential()

model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(timesteps, features)))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(Dropout(0.5))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(outputs, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

early = EarlyStopping(monitor='accuracy', min_delta=0, patience=3, verbose=1, mode='auto')

model.fit(trainX, trainY, epochs=10, verbose=1, callbacks=[early])
print("[!] Training done!")

_, accuracy = model.evaluate(testX, testY, verbose=1)
print(f'Test accurracy : {accuracy:.3f}')
