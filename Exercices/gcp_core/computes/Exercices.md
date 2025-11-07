### Exercice 1: Première VM de Traitement

**Objectif**: Configurer une VM pour traiter des données

1. Créer une VM e2-standard-2
2. Installer Python, pandas, google-cloud-storage
3. Créer un script qui:
   - Télécharge `transactions_500.csv` depuis GCS
   - Calcule le total des ventes par catégorie
   - Sauvegarde le résultat dans GCS

**Fichiers à utiliser**: transactions/transactions_500.csv

### Exercice 2: Automatisation avec Cron

**Objectif**: Planifier l'exécution automatique

1. Sur la VM, créer un script qui traite les ventes quotidiennes
2. Configurer cron pour l'exécuter à 2h du matin
3. Vérifier l'exécution dans les logs

**Fichiers à utiliser**: data/ventes_2024_01.csv, data/ventes_2024_02.csv

### Exercice 3: Traitement en Batch

**Objectif**: Traiter plusieurs fichiers avec reprise sur erreur

1. Vous avez 50 fichiers CSV à traiter dans GCS
2. Créer un script qui:
   - Les traite un par un
   - Sauvegarde sa progression dans checkpoint.json
   - Reprend où il s'est arrêté en cas d'interruption

**Fichiers à utiliser**: Créer 50 copies des fichiers de ventes
