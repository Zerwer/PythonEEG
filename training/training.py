# Currently using two letters with ~400 samples each with around 60% validation accuracy
# Prediction for better results:
# 1000 samples per letter 65%
# 2000 samples per letter 70%
# 3000 samples per letter 75%
import numpy as np
import os
from keras.layers import Dense, Flatten, Dropout
from keras.models import Sequential

# Declare blank sets
x_train = []
y_train = []

x_valid = []
y_valid = []


# Takes fft array and filters frequencies above 45 Hz
def fft_filter_high_frequencies(raw_values):
    fft_data = np.abs(np.fft.rfft(raw_values))
    fft_freq = np.fft.rfftfreq(1500, d=1. / 1500)
    # TODO simplify by removing n elements from end
    return fft_data


# Prepare training set
for file in os.listdir('letters'):
    if file[:1] == 'a':
        y_train.append(1)
    else:
        y_train.append(0)
    # Use fft and collect real numbers divided by 85000 to get input float
    x_train.append(fft_filter_high_frequencies(np.genfromtxt('letters/'+file, delimiter=',')))
    x_train.append(np.abs(np.fft.rfft(np.genfromtxt('letters/'+file, delimiter=',')))/85000)

x_train = np.expand_dims(np.array(x_train), 3)
y_train = np.array(y_train)

# Prepare validation set
for file in os.listdir('validation'):
    if file[:1] == 'a':
        y_valid.append(1)
    else:
        y_valid.append(0)
    # Use fft and collect real numbers divided by 85000 to get input float
    x_valid.append(np.abs(np.fft.rfft(np.genfromtxt('validation/'+file, delimiter=',')))/85000)

x_valid = np.expand_dims(np.array(x_valid), 3)
y_valid = np.array(y_valid)

# Create model
model = Sequential([
    Flatten(input_shape=(751, 1)),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, validation_data=(x_valid, y_valid), shuffle=True, batch_size=32, epochs=200)

# Save mode (results currently good enough to be considered non-random)
model.save('model.h5')
