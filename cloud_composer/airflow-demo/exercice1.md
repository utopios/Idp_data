# Exercice 1 – Pipeline d’ingestion simple avec Apache Airflow


Vous travaillez comme Data Engineer dans une équipe qui souhaite déclencher chaque jour un petit pipeline permettant :

1. d’extraire une liste de données depuis une source simulée (fichier JSON local ou données codées en dur) ;
2. de transformer ces données (normalisation, filtrage simple) ;
3. de charger le résultat transformé dans un fichier CSV local que d’autres équipes pourront utiliser.

Ce pipeline doit être automatisé quotidiennement avec Airflow.

---

# Instructions à réaliser

## 1. Créer un nouveau DAG Airflow

Nom du DAG : `ingestion_pipeline_v1`
Exigences :

* utiliser le TaskFlow API (`@dag`, `@task`) ;
* exécution quotidienne (`schedule="@daily"`) ;
* `catchup=False` ;
* date de départ : `start_date=datetime(2024, 1, 1)`.

---

## 2. Créer une tâche d'extraction

Créer une fonction décorée avec `@task` qui :

* simule une extraction de données ;
* retourne une liste de dictionnaires Python.

Exemple attendu (mais à coder vous-même) :

```python
[
    {"name": "Alice", "age": 34},
    {"name": "Bob", "age": 19},
    {"name": "Charlie", "age": 42}
]
```

Cette valeur doit être renvoyée, ce qui signifie qu’elle sera automatiquement poussée dans XCom par Airflow.

---

## 3. Créer une tâche de transformation

Créer une deuxième tâche `@task` qui :

* prend en entrée les données extraites (Airflow gère l’XCom automatiquement) ;
* filtre uniquement les personnes de plus de 20 ans ;
* ajoute un champ `category` basé sur l’âge :

  * moins de 30 ans : `"young"`
  * 30 ans ou plus : `"adult"`

Elle doit renvoyer la liste transformée.

---

## 4. Créer une tâche de chargement

Créer une troisième tâche `@task` qui :

* reçoit les données transformées ;
* crée un fichier CSV dans un répertoire local nommé `data/` ;
* le fichier doit contenir les colonnes : `name`, `age`, `category` ;
* le nom du fichier doit inclure la date d’exécution Airflow, par exemple :
  `data/output_2024-01-10.csv`.

La tâche doit afficher dans les logs où le fichier a été sauvegardé.

---

## 5. Ajouter une quatrième tâche Bash (optionnelle mais demandée)

Ajouter une tâche `BashOperator` qui :

* affiche un message dans les logs Airflow ;
* attend 3 secondes (commande `sleep 3`) ;
* confirme que le fichier CSV existe via `ls data/`.

Cette tâche doit s’exécuter après le chargement.

---

## 6. Orchestration

Ordonner les tâches comme suit :

```
extract -> transform -> load -> check_file
```



# Bonus (facultatif)

1. Ajouter une gestion simple d’erreur dans la transformation.
2. Ajouter un test pour vérifier que l’extraction n’est pas vide (sinon lever une exception).
3. Faire une version parallèle où la transformation crée deux fichiers CSV différents (par catégorie).
4. Ajouter une métrique simple renvoyée par XCom (ex: nombre de lignes transformées).
