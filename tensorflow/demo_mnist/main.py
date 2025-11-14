import tensorflow as tf
from tensorflow.keras import Input, Model, layers
from tensorflow.keras.layers import Dense, Concatenate
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from tensorflow.keras.datasets import mnist


(X_train, y_train), (X_test, y_test) = mnist.load_data()

print("="*50)
print("Exploration des données")
print("="*50)
print(f"X_train shape: {X_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"Labels uniques dans y_train: {np.unique(y_train)}")

X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0
X_train = X_train.reshape(-1, 28*28)
X_test = X_test.reshape(-1, 28*28)

print("="*50)
print("Après prétaitement des données")
print("="*50)
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")  

model = tf.keras.Sequential([
    layers.Input(shape=(28*28,)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.1),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.1),
    layers.Dense(10, activation='softmax')
    ], name="mnist_model")

model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("="*50)
print("Entraînement du modèle")
print("="*50)
history = model.fit(X_train, y_train, epochs=5, batch_size=128, validation_split=0.1, verbose=1)
print("="*50)
print("Évaluation du modèle")
print("="*50)
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(f'\nTest accuracy: {test_acc}')

# Sauvegarde du modèle
model.save('mnist_model.keras')
print("Modèle sauvegardé sous le nom 'mnist_model.keras'")