#!/bin/bash

# Script de collecte automatique des publications
# Ce script est exécuté périodiquement par cron pour collecter les publications

# Activation de l'environnement virtuel Python
source /opt/challenge-convention/venv/bin/activate

# Exécution du script de collecte
cd /opt/challenge-convention
python -c "
from src.main import create_app
from src.routes.collecte import collecter_publications_instagram, collecter_publications_linkedin
import logging

# Configuration du logging
logging.basicConfig(
    filename='/opt/challenge-convention/logs/collecte.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('collecte_cron')

# Création de l'application Flask
app = create_app()

# Exécution de la collecte dans le contexte de l'application
with app.app_context():
    logger.info('Début de la collecte automatique')
    try:
        collecter_publications_instagram()
        logger.info('Collecte Instagram terminée')
    except Exception as e:
        logger.error(f'Erreur lors de la collecte Instagram: {str(e)}')
    
    try:
        collecter_publications_linkedin()
        logger.info('Collecte LinkedIn terminée')
    except Exception as e:
        logger.error(f'Erreur lors de la collecte LinkedIn: {str(e)}')
    
    logger.info('Fin de la collecte automatique')
"

# Sortie de l'environnement virtuel
deactivate
