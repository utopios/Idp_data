import tensorflow as tf
import numpy as np

batch_images = tf.random.uniform(shape=(10,28,28, 1), minval=0, maxval=1)  
print("Batch d'images aléatoires:\n", batch_images.numpy())
# 2. Normalisation des images
mean = tf.reduce_mean(batch_images)
print("Moyenne des pixels:", mean.numpy())
stddev = tf.math.reduce_std(batch_images)
print("Écart-type des pixels:", stddev.numpy())
batch_images_normalized = (batch_images - mean) / stddev
print("Batch d'images normalisées:\n", batch_images_normalized.numpy())

# 3. Extraction
first_five = batch_images[:5]
print("Premières 5 images normalisées:\n", first_five.numpy())
first_five_gathered = tf.gather(batch_images_normalized, indices=[x for x in range(5)])
# 4. Différence avec la moyenne
difference_from_mean = batch_images - tf.reduce_mean(batch_images, axis=0, keepdims=True) #  [1,28,28,1]
print("Différence par rapport à la moyenne:\n", difference_from_mean.numpy())
# 5. Reshape
batch_flat = tf.reshape(batch_images, [10, 784])
print("Batch d'images aplaties:\n", batch_flat.numpy())