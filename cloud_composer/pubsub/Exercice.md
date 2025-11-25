# Sujet d’exercice : Pipeline de collecte d’événements avec Google Pub/Sub

## Contexte

Une entreprise souhaite mettre en place une première brique de son pipeline de données en collectant des événements provenant d’une application mobile.
Chaque événement contient des informations sur l’activité de l’utilisateur (page consultée, durée, type d’action, timestamp, identifiant utilisateur).

L’objectif de cet exercice est de simuler un flux d’événements, de les envoyer dans Pub/Sub, puis de les consommer pour les stocker ou les préparer à une future intégration dans un Data Lake.

---

### 1. Création de l’infrastructure Pub/Sub

Dans le projet GCP du formateur ou du stagiaire, créer :

* Un **topic** nommé `events-topic`
* Une **subscription** en mode pull nommée `events-sub`

Les stagiaires doivent :

* Activer l’API Pub/Sub
* Créer un compte de service avec une clé JSON
* Donner les rôles minimums : Pub/Sub Publisher et Pub/Sub Subscriber

---

### 2. Simulation d’un flux d’événements

Écrire un script Python `publisher.py` qui :

1. Génère des événements JSON tels que :

   * user_id
   * event_type (`login`, `view_page`, `click`, `logout`)
   * page (facultatif)
   * timestamp
2. Envoie un message toutes les 200 à 500 ms dans Pub/Sub.

Exemple de message attendu :

```json
{
  "user_id": 42,
  "event_type": "view_page",
  "page": "/products/123",
  "timestamp": "2025-03-21T14:22:10Z"
}
```

Le script doit envoyer entre 20 et 50 événements.

---

### 3. Consommation et traitement des messages

Écrire un script `consumer.py` qui :

1. Écoute la subscription `events-sub`
2. Récupère les messages
3. Les affiche de façon formatée en console
4. Stocke chaque événement dans un fichier local `events.log` sous format JSONL (un JSON par ligne)
5. Acknowledge chaque message

---

### 4. Analyse rapide des données collectées

Écrire un petit script ou quelques lignes Python (ou SQL local si souhaité) qui :

* lit le fichier `events.log`
* calcule :

  * le nombre total d’événements
  * la répartition par `event_type`
  * la liste des pages les plus vues (si applicables)
  * le nombre d’utilisateurs uniques

Exemple attendu :

```
Total events collected: 48
Unique users: 12
Event distribution:
  login: 12
  view_page: 25
  click: 8
  logout: 3
```

---

## Livrables attendus

* `publisher.py`
* `consumer.py`
* `events.log`
* Un bref fichier texte `analysis.txt` expliquant les résultats obtenus et les difficultés rencontrées.
