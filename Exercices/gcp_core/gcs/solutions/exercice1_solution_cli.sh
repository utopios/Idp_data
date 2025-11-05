#!/bin/bash

BUCKET_NAME="ihab_bucket_utopios"
PROJECT_ID="projet-kube-c"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Exercice 1: Organisation du Data Lake ===${NC}"

# echo -e "\n${GREEN}[1/4] Création du bucket${NC}"
# gsutil mb -p $PROJECT_ID -c STANDARD -l europe-west1 gs://$BUCKET_NAME

# if [ $? -eq 0 ]; then
#     echo "Bucket créé avec succès"
# else
#     echo "Erreur lors de la création du bucket"
#     exit 1
# fi

echo -e "\n${GREEN}[2/4] Ajout de tags au bucket${NC}"
gsutil label set of:m2i gs://$BUCKET_NAME
gsutil label ch -l type:data-lake gs://$BUCKET_NAME
gsutil label ch -l department:analytics gs://$BUCKET_NAME

echo "Tags ajoutés au bucket"

echo -e "\nLabels du bucket:"
gsutil label get gs://$BUCKET_NAME

echo -e "\n${GREEN}[3/4] Création de la structure de dossiers${NC}"

echo "Structure créée le $(date)" | gsutil cp - gs://$BUCKET_NAME/raw/ventes/2024/01/.keep
echo "Structure créée le $(date)" | gsutil cp - gs://$BUCKET_NAME/raw/ventes/2024/02/.keep
echo "Structure créée le $(date)" | gsutil cp - gs://$BUCKET_NAME/raw/logs/2024/01/.keep
echo "Structure créée le $(date)" | gsutil cp - gs://$BUCKET_NAME/processed/.keep
echo "Structure créée le $(date)" | gsutil cp - gs://$BUCKET_NAME/archive/.keep

echo "Structure de dossiers créée"

echo -e "\n${GREEN}[4/4] Upload des fichiers${NC}"

echo "Upload des fichiers de ventes..."
gsutil cp ../Exercice1/ventes_2024_01.csv gs://$BUCKET_NAME/raw/ventes/2024/01/
gsutil cp ../Exercice1/ventes_2024_02.csv gs://$BUCKET_NAME/raw/ventes/2024/02/

echo "Upload des fichiers de logs..."
gsutil cp ../Exercice1/logs/*.log gs://$BUCKET_NAME/raw/logs/2024/01/

echo "Fichiers uploadés avec succès"

echo -e "\n${BLUE}=== Vérification de la structure ===${NC}"
gsutil ls -r gs://$BUCKET_NAME

echo -e "\n${BLUE}=== Statistiques du bucket ===${NC}"
gsutil du -sh gs://$BUCKET_NAME

echo -e "\n${BLUE}=== Informations du bucket ===${NC}"
gsutil ls -L -b gs://$BUCKET_NAME

echo -e "\n${GREEN}Exercice 1 terminé avec succès!${NC}"
echo -e "\nCommandes utiles:"
echo -e "  - Lister le contenu: ${BLUE}gsutil ls -r gs://$BUCKET_NAME${NC}"
echo -e "  - Supprimer le bucket: ${BLUE}gsutil rm -r gs://$BUCKET_NAME${NC}"
echo -e "  - Voir les labels: ${BLUE}gsutil label get gs://$BUCKET_NAME${NC}"
