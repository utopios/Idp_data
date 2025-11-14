# Workshop : Analyse de sentiments IMDB avec Keras

## 1. Objectifs du workshop

Dans ce workshop, vous devez :

1. Charger un jeu de données texte intégré à Keras : IMDB (critiques de films).
2. Préparer les données sous forme de séquences numériques (padding).
3. Construire un modèle de deep learning simple pour la classification binaire (positif / négatif).
4. Compiler, entraîner et évaluer le modèle.
5. Analyser les résultats et tester quelques prédictions.

---

## 2. Pré-requis techniques

* Python 3.x
* TensorFlow 2.x (avec Keras intégré)
* Notions de base sur :

  * classification binaire
  * réseau de neurones simple
  * train / test

---

## Étape 0 – Imports et configuration

Objectif : importer les bibliothèques nécessaires.


```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import pad_sequences

import numpy as np

print("Version de TensorFlow :", tf.__version__)
```

---

## Étape 1 – Chargement du jeu de données IMDB

Objectif : utiliser un dataset non visuel intégré à Keras.

Keras fournit le dataset IMDB déjà tokenisé : chaque critique est une liste d’indices de mots.
On limite le vocabulaire aux N mots les plus fréquents.

1. Charger le dataset IMDB avec `keras.datasets.imdb.load_data`.
2. Limiter le vocabulaire aux 10 000 mots les plus fréquents.
3. Afficher les tailles de `X_train`, `y_train`, `X_test`, `y_test`.

Code squelette :

```python
# Nombre maximum de mots dans le vocabulaire
vocab_size = 10_000

# TODO: charger les données IMDB avec num_words=vocab_size
# Indice: utiliser keras.datasets.imdb.load_data
imdb = keras.datasets.imdb
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)

print("Taille X_train :", len(X_train))
print("Taille y_train :", len(y_train))
print("Taille X_test  :", len(X_test))
print("Taille y_test  :", len(y_test))

# Afficher la première critique (version indices) et son label
print("Exemple de critique (indices) :", X_train[0][:20], "...")
print("Label correspondant :", y_train[0])
```

Questions :

* Que représente chaque entier dans la liste `X_train[0]` ?
* Que signifie un label 0 ? Un label 1 ?

---

## Étape 2 – Décodage optionnel d’une critique (pour compréhension)

Objectif : montrer comment mapper les indices vers les mots, pour aider à comprendre.


```python
# Récupérer le dictionnaire mot -> indice
word_index = imdb.get_word_index()

# Inverser le mapping: indice -> mot
reverse_word_index = {value + 3: key for (key, value) in word_index.items()}
reverse_word_index[0] = "<PAD>"
reverse_word_index[1] = "<START>"
reverse_word_index[2] = "<UNK>"
reverse_word_index[3] = "<UNUSED>"

def decode_review(encoded_review):
    return " ".join(reverse_word_index.get(i, "?") for i in encoded_review)

print("Critique décodée :")
print(decode_review(X_train[0][:100]))
print("Label:", y_train[0])
```

---

## Étape 3 – Préparation des données : padding des séquences

Objectif : toutes les séquences doivent avoir la même longueur pour entrer dans un réseau.


1. Choisir une longueur maximale (par exemple 200 mots).
2. Utiliser `pad_sequences` pour tronquer ou compléter les critiques.

Code squelette :

```python
# Longueur maximale des séquences
maxlen = 200

# TODO: appliquer pad_sequences sur X_train et X_test
# Indice: utiliser pad_sequences avec maxlen=maxlen, padding="post", truncating="post"
X_train_padded = pad_sequences(
    X_train,
    maxlen=maxlen,
    padding="post",
    truncating="post"
)

X_test_padded = pad_sequences(
    X_test,
    maxlen=maxlen,
    padding="post",
    truncating="post"
)

print("Forme de X_train_padded :", X_train_padded.shape)
print("Forme de X_test_padded  :", X_test_padded.shape)
```

* Pourquoi doit-on appliquer un padding ?
* Quelle est la différence entre `padding="post"` et `padding="pre"` ?

---

## Étape 4 – Construction du modèle

Objectif : construire un modèle de classification binaire avec :

* une couche Embedding
* une étape de réduction (par exemple GlobalAveragePooling1D)
* une ou deux couches Dense
* une sortie sigmoïde

1. Utiliser `keras.Sequential`.
2. Ajouter une couche `Embedding` avec :

   * `input_dim=vocab_size`
   * `output_dim=embedding_dim` (par exemple 32)
   * `input_length=maxlen`
3. Ajouter une couche de réduction, par exemple `GlobalAveragePooling1D` (simple) ou un `Conv1D + GlobalMaxPooling1D`.
4. Ajouter une couche Dense cachée avec `relu`.
5. Ajouter une couche Dense de sortie avec 1 neurone et `activation="sigmoid"`.


```python
embedding_dim = 32

model = keras.Sequential(name="IMDB_Sentiment_Classifier")

# TODO: ajouter une couche Embedding
# Indice: layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=maxlen)
model.add(layers.Embedding(input_dim=vocab_size,
                           output_dim=embedding_dim,
                           input_length=maxlen))

# TODO: ajouter une couche GlobalAveragePooling1D (ou autre pooling)
model.add(layers.GlobalAveragePooling1D())

# TODO: ajouter une couche Dense cachée avec relu (par ex. 16 neurones)
model.add(layers.Dense(16, activation="relu"))

# TODO: ajouter une couche de sortie (1 neurone, sigmoid)
model.add(layers.Dense(1, activation="sigmoid"))

model.summary()
```

* À quoi sert la couche Embedding ?
* Pourquoi la sortie a-t-elle 1 seul neurone avec une sigmoïde ?

---

## Étape 5 – Compilation du modèle

Objectif : préparer le modèle pour l’entraînement.

Consignes :

* Optimizer : `adam`
* Loss : `binary_crossentropy` (classification binaire)
* Metrics : `accuracy`


```python
# TODO: compiler le modèle
# Indice: optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
```


* Pourquoi ne pas utiliser `sparse_categorical_crossentropy` ici ?
* Quelle est la différence entre classification binaire et multi-classe dans ce contexte ?

---

## Étape 6 – Entraînement du modèle

Objectif : entraîner le modèle sur les données d’entraînement et suivre la validation.

* Utiliser `model.fit`.
* Par exemple, 5 epochs, batch_size=512.
* Utiliser `validation_split=0.2` ou `validation_data=(X_test_padded, y_test)`.


```python
batch_size = 512
epochs = 5

history = model.fit(
    X_train_padded,
    y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_split=0.2,  # ou validation_data=(X_test_padded, y_test)
    verbose=1
)
```

Tracer les courbes d’entraînement.

```python
import matplotlib.pyplot as plt

def plot_history(history):
    history_dict = history.history
    acc = history_dict["accuracy"]
    val_acc = history_dict["val_accuracy"]
    loss = history_dict["loss"]
    val_loss = history_dict["val_loss"]
    epochs_range = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, loss, label="loss entraînement")
    plt.plot(epochs_range, val_loss, label="loss validation")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, acc, label="acc entraînement")
    plt.plot(epochs_range, val_acc, label="acc validation")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()

    plt.show()

plot_history(history)
```

* Voit-on de l’overfitting ? À partir de quelle epoch ?
* Faut-il arrêter plus tôt ou régulariser davantage ?

---

## Étape 7 – Évaluation sur le jeu de test

Objectif : mesurer la performance finale sur les données de test.


```python
test_loss, test_acc = model.evaluate(X_test_padded, y_test, verbose=0)
print("Loss sur test :", test_loss)
print("Accuracy sur test :", test_acc)
```


* L’accuracy test est-elle proche de l’accuracy validation ?
* Si non, quelles peuvent être les raisons ?

---

## Étape 8 – Tester des prédictions sur quelques critiques

Objectif : voir concrètement comment le modèle se comporte.

1. Prendre quelques indices dans `X_test`.
2. Prédire la probabilité que la critique soit positive.
3. Comparer avec le label réel.

Code squelette :

```python
# Choisir quelques indices de test
indices = [0, 1, 2, 3, 4]

for idx in indices:
    review = X_test_padded[idx:idx+1]  # garder la dimension batch
    prob = model.predict(review)[0][0]
    prediction = 1 if prob >= 0.5 else 0

    print("Critique index :", idx)
    print("Probabilité positive prédite :", prob)
    print("Prédiction du modèle (0=neg, 1=pos) :", prediction)
    print("Label réel :", y_test[idx])
    print("-" * 50)
```

Optionnel : afficher aussi la critique décodée avec `decode_review`.

---

## Questions 

1. Quelles sont les différences principales entre ce problème et MNIST ?
2. Pourquoi le prétraitement (tokenisation, padding, embedding) est-il plus complexe ici ?
3. Quelles améliorations possibles pour le modèle ?
4. Comment utiliser ce type de modèle sur des données texte d’une vraie application (avis clients, tickets support, etc.) ?
