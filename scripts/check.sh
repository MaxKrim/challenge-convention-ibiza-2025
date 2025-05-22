#!/bin/bash

# Script de vérification pour l'application Challenge Convention Ibiza 2025
# Ce script vérifie que tous les composants sont correctement installés et configurés

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages d'information
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Fonction pour afficher les avertissements
warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

# Fonction pour afficher les erreurs
error() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

# Vérification des privilèges root
if [ "$(id -u)" != "0" ]; then
   error "Ce script doit être exécuté avec les privilèges root (sudo)."
   exit 1
fi

# Vérification de l'installation
info "Vérification de l'installation..."

# Vérification des dépendances
info "Vérification des dépendances..."
DEPS_OK=true

for dep in python3 python3-pip nginx supervisor; do
    if ! dpkg -l | grep -q $dep; then
        error "Dépendance manquante: $dep"
        DEPS_OK=false
    fi
done

if [ "$DEPS_OK" = true ]; then
    info "Toutes les dépendances sont installées."
else
    warning "Certaines dépendances sont manquantes. Exécutez le script d'installation."
fi

# Vérification des fichiers de l'application
info "Vérification des fichiers de l'application..."
FILES_OK=true

if [ ! -d "/opt/challenge-convention" ]; then
    error "Répertoire d'installation manquant: /opt/challenge-convention"
    FILES_OK=false
fi

if [ ! -f "/opt/challenge-convention/config.env" ]; then
    error "Fichier de configuration manquant: /opt/challenge-convention/config.env"
    FILES_OK=false
fi

if [ ! -d "/opt/challenge-convention/venv" ]; then
    error "Environnement virtuel Python manquant: /opt/challenge-convention/venv"
    FILES_OK=false
fi

if [ "$FILES_OK" = true ]; then
    info "Tous les fichiers de l'application sont présents."
else
    warning "Certains fichiers de l'application sont manquants. Exécutez le script d'installation."
fi

# Vérification des services
info "Vérification des services..."
SERVICES_OK=true

if ! systemctl is-active --quiet nginx; then
    error "Le service nginx n'est pas actif."
    SERVICES_OK=false
fi

if ! supervisorctl status challenge-convention | grep -q "RUNNING"; then
    error "L'application challenge-convention n'est pas en cours d'exécution."
    SERVICES_OK=false
fi

if [ "$SERVICES_OK" = true ]; then
    info "Tous les services sont actifs et fonctionnent correctement."
else
    warning "Certains services ne fonctionnent pas correctement."
fi

# Vérification de l'accès web
info "Vérification de l'accès web..."
IP_ADDRESS=$(hostname -I | awk '{print $1}')

if curl -s --head "http://$IP_ADDRESS" | grep "200 OK" > /dev/null; then
    info "L'application est accessible via http://$IP_ADDRESS"
else
    warning "L'application n'est pas accessible via http://$IP_ADDRESS"
fi

# Vérification de la base de données
info "Vérification de la base de données..."
if [ -f "/opt/challenge-convention/instance/challenge.db" ]; then
    info "La base de données existe."
else
    warning "La base de données n'existe pas encore. Elle sera créée au premier démarrage de l'application."
fi

# Vérification des sauvegardes
info "Vérification des sauvegardes..."
if [ -d "/opt/challenge-convention/backups" ]; then
    BACKUP_COUNT=$(ls -1 /opt/challenge-convention/backups/*.tar.gz 2>/dev/null | wc -l)
    info "Nombre de sauvegardes trouvées: $BACKUP_COUNT"
else
    warning "Aucune sauvegarde n'a encore été effectuée."
fi

# Vérification des tâches planifiées
info "Vérification des tâches planifiées..."
if crontab -l | grep -q "challenge-convention"; then
    info "Les tâches planifiées sont configurées."
else
    warning "Les tâches planifiées ne sont pas configurées."
fi

# Résumé
echo ""
echo "=== RÉSUMÉ DE LA VÉRIFICATION ==="
if [ "$DEPS_OK" = true ] && [ "$FILES_OK" = true ] && [ "$SERVICES_OK" = true ]; then
    info "L'application est correctement installée et configurée."
    echo ""
    echo "Vous pouvez accéder à l'application à l'adresse:"
    echo "http://$IP_ADDRESS"
    echo ""
    echo "Interface d'administration:"
    echo "http://$IP_ADDRESS/admin"
else
    warning "L'application n'est pas correctement installée ou configurée."
    echo ""
    echo "Exécutez le script d'installation pour résoudre les problèmes:"
    echo "sudo /opt/challenge-convention/scripts/install.sh"
fi
