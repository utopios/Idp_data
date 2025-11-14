import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
import os

def predict_digit(model_path, image_path):
    # Charger le modèle
    model = keras.models.load_model(model_path)
    model.summary()
    # Charger et prétraiter l'image
    img = keras.preprocessing.image.load_img(image_path, color_mode='grayscale', target_size=(28, 28))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = img_array.reshape(1, 28*28)  # Reshape pour correspondre à l'entrée du modèle

    # Faire une prédiction
    predictions = model.predict(img_array)
    predicted_digit = np.argmax(predictions, axis=1)
    print("Prédictions brutes :", predictions)
    print(f'Le chiffre prédit est : {predicted_digit}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python predict.py <model_path> <image_path>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    image_path = sys.argv[2]
    
    if not os.path.exists(model_path):
        print(f"Le modèle spécifié n'existe pas : {model_path}")
        sys.exit(1)
    
    if not os.path.exists(image_path):
        print(f"L'image spécifiée n'existe pas : {image_path}")
        sys.exit(1)
    
    predict_digit(model_path, image_path)