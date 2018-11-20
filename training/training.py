import numpy as np
import os
from keras.layers import Dense, Flatten, Dropout
from keras.models import Sequential

x_train = []
y_train = []

x_valid = []
y_valid = []

for file in os.listdir('letters'):
    if file[:1] == 'a':
        y_train.append(0)
    else:
        y_train.append(1)
    x_train.append(np.abs(np.fft.rfft(np.genfromtxt('letters/'+file, delimiter=',')))/85000)

x_train = np.expand_dims(np.array(x_train), 3)
y_train = np.array(y_train)

for file in os.listdir('validation'):
    if file[:1] == 'a':
        y_valid.append(0)
    else:
        y_valid.append(1)
    x_valid.append(np.abs(np.fft.rfft(np.genfromtxt('validation/'+file, delimiter=',')))/85000)

x_valid = np.expand_dims(np.array(x_valid), 3)
y_valid = np.array(y_valid)

model = Sequential([
    Flatten(input_shape=(751, 1)),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, validation_data=(x_valid, y_valid), shuffle=True, batch_size=30, epochs=1000)
model.save('model.h5')
