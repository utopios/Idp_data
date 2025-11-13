import tensorflow as tf
# print(f"TensorFlow version: {tf.__version__}")
# print(f"GPU disponible: {tf.config.list_physical_devices('GPU')}")
# print(f"Eager execution: {tf.executing_eagerly()}")

# Scalaire
# scalaire = tf.constant(42)
# print(scalaire.shape)  # ()
# print(scalaire.numpy())  # 42
# print(scalaire.dtype)  # <dtype: 'int32'>
# # Vecteur
# vecteur = tf.constant([1, 2, 3, 4, 5])
# print(vecteur.shape)  # (5,)
# print(vecteur.numpy())  # [1 2 3 4 5]
# # Matrice
# matrice = tf.constant([[1, 2], [3, 4], [5, 6]])
# print(matrice.shape)  # (3, 2)
# print(matrice.numpy())  # [[1 2] [3 4] [5 6]]

# # Tensore 3D
# tensore_3d = tf.constant([[[1], [2]], [[3], [4]], [[5], [6]]])
# print(tensore_3d.shape)  # (3, 2, 1)
# print(tensore_3d.numpy())

# # Création de tenseurs avec des valeurs spécifiques
# zeros = tf.zeros((2, 3))
# print("Tenseur de zéros:\n", zeros.numpy())

a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
# Opérations élément par élément
addition = tf.add(a, b)          # ou a + b
print("Addition:\n", addition.numpy())
soustraction = tf.subtract(a, b) # ou a - b
print("Soustraction:\n", soustraction.numpy())
multiplication = tf.multiply(a, b) # ou a * b
print("Multiplication:\n", multiplication.numpy())
division = tf.divide(a, b)       # ou a / b
print("Division:\n", division.numpy())
# Opérations matricielles
matmul = tf.matmul(a, b)         # Produit matriciel
print("Produit matriciel:\n", matmul.numpy())
transpose = tf.transpose(a)
print("Transposée de a:\n", transpose.numpy())