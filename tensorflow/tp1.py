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
