import numpy as np
from keras.models import Sequential
from keras.layers import Dense, InputLayer

model = Sequential([
    InputLayer((10,)),
    Dense(6, activation='relu'),
    Dense(3, activation='relu'),
    Dense(1, activation='relu')
])
model.compile(optimizer='adam', loss='mse')
X = np.random.random((1000, 10))
y = np.random.random((1000,))
model.fit(X, y, epochs=100)
