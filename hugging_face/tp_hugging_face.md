
# TP : Classification de genre sur images

Vous deverez rechercher, sélectionner et utiliser un modèle de classification d'images sur Hugging Face pour déterminer si une photo représente un homme ou une femme.

### Contexte
Vous travaillez pour une application de tri automatique de photos. Votre mission est de développer un prototype permettant d'identifier le genre des personnes sur les photos.

### Partie 1 : Recherche du modèle

**Consignes :**
1. Accédez au Hub Hugging Face : https://huggingface.co/models
2. Recherchez un modèle approprié en utilisant les filtres :
   - Task : `Image Classification`
   - Mots-clés : "gender", "face", "person"
3. Identifiez au moins 3 modèles candidats
4. Pour chaque modèle, documentez :
   - Le nom du modèle
   - Le nombre de téléchargements
   - La date de dernière mise à jour
   - Les classes qu'il peut prédire
   - Les limitations éventuelles

**Questions de réflexion :**
- Quels critères utilisez-vous pour choisir un modèle ?
- Le modèle est-il entraîné sur des données représentatives ?
- Y a-t-il des biais potentiels à considérer ?

### Partie 2 : Installation et configuration 


### Partie 3 : Développement du script

Créez un script Python `gender_classifier.py` qui :

1. **Charge le modèle** sélectionné depuis Hugging Face
2. **Accepte une image en entrée** (via chemin de fichier)
3. **Affiche les résultats** avec les probabilités
4. **Gère les erreurs** potentielles (fichier non trouvé, format invalide)


### Partie 4 : Analyse critique

**Questions à traiter dans un document Markdown :**

1. **Performance**
   - Quel est le taux de réussite global ?
   - Sur quels types d'images le modèle échoue-t-il ?

2. **Biais et éthique**
   - Le modèle présente-t-il des biais (âge, ethnie, etc.) ?
   - Quelles sont les implications éthiques de ce type de classification ?
   - Dans quels contextes ce modèle devrait-il être utilisé ou évité ?

3. **Améliorations possibles**
   - Comment améliorer les performances ?
   - Quelles données supplémentaires seraient nécessaires ?

