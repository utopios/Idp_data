### Exercice : Calcul de gradient et descente de gradient avec TensorFlow

#### Objectif

Mettre en œuvre le calcul automatique de gradient avec `tf.GradientTape` et appliquer une descente de gradient pour trouver le minimum d’une fonction donnée.

---

#### Énoncé

1. Écrire une fonction TensorFlow :
   ( f(x) = x^2 - 4x + 5 )

2. Initialiser une variable `x` avec une valeur de départ (par exemple 0.0).

3. Utiliser `tf.GradientTape` pour calculer le gradient de ( f(x) ) par rapport à `x`.

4. Mettre à jour la variable `x` à l’aide de la règle de descente de gradient :

   ( x = x - (\text{learning_rate} \times \text{gradient}) )

5. Répéter la mise à jour pendant plusieurs itérations afin de faire converger `x` vers le minimum.

6. Afficher à chaque étape la valeur de `x`, de `f(x)` et du gradient.

7. Tracer la courbe de ( f(x) ) et la trajectoire de `x` au fil des itérations.

---

#### Extensions possibles

* Modifier la fonction pour une autre expression, par exemple :
  ( f(x) = x^3 - 6x^2 + 9x + 15 )
* Expérimenter différents taux d’apprentissage.
* Étendre l’exercice à une fonction de deux variables ( f(x, y) ) et représenter les contours du gradient.
