#!/bin/bash

# Script d'installation automatique pour l'application Challenge Convention Ibiza 2025
# Ce script installe et configure tous les composants nécessaires sur un VPS Ubuntu

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

# Mise à jour du système
info "Mise à jour du système..."
apt update && apt upgrade -y

# Installation des dépendances
info "Installation des dépendances..."
apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git supervisor

# Création du répertoire d'installation
info "Création du répertoire d'installation..."
mkdir -p /opt/challenge-convention
cd /opt/challenge-convention

# Téléchargement de l'application
info "Téléchargement de l'application..."
git clone https://github.com/votre-compte/challenge-convention.git .
# Note: Dans une version réelle, ce serait un dépôt GitHub ou un fichier ZIP téléchargé

# Création de l'environnement virtuel Python
info "Configuration de l'environnement Python..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configuration de l'application
info "Configuration de l'application..."
mkdir -p logs
mkdir -p instance

# Création du fichier de configuration
cat > config.env << EOF
FLASK_APP=src.main
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
ADMIN_USERNAME=admin
ADMIN_PASSWORD=challenge2025
DATABASE_URL=sqlite:///instance/challenge.db
EOF

# Configuration de Supervisor
info "Configuration du gestionnaire de processus..."
cat > /etc/supervisor/conf.d/challenge-convention.conf << EOF
[program:challenge-convention]
directory=/opt/challenge-convention
command=/opt/challenge-convention/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 "src.main:create_app()"
autostart=true
autorestart=true
stderr_logfile=/opt/challenge-convention/logs/supervisor.err.log
stdout_logfile=/opt/challenge-convention/logs/supervisor.out.log
environment=
    FLASK_APP="src.main",
    FLASK_ENV="production",
    SECRET_KEY="$(grep SECRET_KEY config.env | cut -d '=' -f2)",
    ADMIN_USERNAME="$(grep ADMIN_USERNAME config.env | cut -d '=' -f2)",
    ADMIN_PASSWORD="$(grep ADMIN_PASSWORD config.env | cut -d '=' -f2)",
    DATABASE_URL="$(grep DATABASE_URL config.env | cut -d '=' -f2)"
EOF

# Configuration de Nginx
info "Configuration du serveur web..."
cat > /etc/nginx/sites-available/challenge-convention << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /opt/challenge-convention/src/static;
    }
}
EOF

# Activation de la configuration Nginx
ln -sf /etc/nginx/sites-available/challenge-convention /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Création des scripts utilitaires
info "Création des scripts utilitaires..."

# Script de configuration du domaine
cat > scripts/setup-domain.sh << 'EOF'
#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 votre-domaine.com"
    exit 1
fi

DOMAIN=$1

# Mise à jour de la configuration Nginx
sed -i "s/server_name _;/server_name $DOMAIN;/" /etc/nginx/sites-available/challenge-convention

# Redémarrage de Nginx
systemctl restart nginx

# Configuration de Let's Encrypt
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

echo "Configuration du domaine $DOMAIN terminée avec succès!"
EOF
chmod +x scripts/setup-domain.sh

# Script de sauvegarde
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/challenge-convention/backups"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/backup-$DATE.tar.gz"

mkdir -p $BACKUP_DIR

# Sauvegarde de la base de données et des fichiers importants
tar -czf $BACKUP_FILE /opt/challenge-convention/instance /opt/challenge-convention/config.env

echo "Sauvegarde créée : $BACKUP_FILE"
EOF
chmod +x scripts/backup.sh

# Script de restauration
cat > scripts/restore-backup.sh << 'EOF'
#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 YYYY-MM-DD"
    exit 1
fi

DATE=$1
BACKUP_DIR="/opt/challenge-convention/backups"
BACKUP_FILE="$BACKUP_DIR/backup-$DATE.tar.gz"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Erreur: Le fichier de sauvegarde $BACKUP_FILE n'existe pas."
    exit 1
fi

# Arrêt des services
supervisorctl stop challenge-convention

# Restauration des fichiers
tar -xzf $BACKUP_FILE -C /

# Redémarrage des services
supervisorctl start challenge-convention

echo "Restauration terminée avec succès!"
EOF
chmod +x scripts/restore-backup.sh

# Script de mise à jour
cat > scripts/update.sh << 'EOF'
#!/bin/bash
cd /opt/challenge-convention

# Sauvegarde avant mise à jour
./scripts/backup.sh

# Mise à jour du code
git pull

# Mise à jour des dépendances
source venv/bin/activate
pip install -r requirements.txt

# Redémarrage des services
supervisorctl restart challenge-convention

echo "Mise à jour terminée avec succès!"
EOF
chmod +x scripts/update.sh

# Script de réinitialisation du mot de passe admin
cat > scripts/reset-admin-password.sh << 'EOF'
#!/bin/bash
echo "Réinitialisation du mot de passe administrateur"
echo -n "Nouveau mot de passe: "
read -s PASSWORD
echo

# Mise à jour du mot de passe dans le fichier de configuration
sed -i "s/ADMIN_PASSWORD=.*/ADMIN_PASSWORD=$PASSWORD/" /opt/challenge-convention/config.env

# Redémarrage des services pour appliquer les changements
supervisorctl restart challenge-convention

echo "Mot de passe administrateur mis à jour avec succès!"
EOF
chmod +x scripts/reset-admin-password.sh

# Configuration des tâches planifiées
info "Configuration des tâches planifiées..."
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/challenge-convention/scripts/backup.sh") | crontab -
(crontab -l 2>/dev/null; echo "*/30 * * * * /opt/challenge-convention/venv/bin/python /opt/challenge-convention/src/cron/collecte.py") | crontab -

# Démarrage des services
info "Démarrage des services..."
systemctl restart nginx
supervisorctl reread
supervisorctl update
supervisorctl restart challenge-convention

# Récupération de l'adresse IP
IP_ADDRESS=$(hostname -I | awk '{print $1}')

# Message final
info "Installation terminée avec succès!"
echo ""
echo "Vous pouvez maintenant accéder à l'application à l'adresse:"
echo "http://$IP_ADDRESS"
echo ""
echo "Interface d'administration:"
echo "http://$IP_ADDRESS/admin"
echo "Identifiants par défaut: admin / challenge2025"
echo ""
warning "N'oubliez pas de changer le mot de passe administrateur!"
echo "Utilisez la commande: sudo /opt/challenge-convention/scripts/reset-admin-password.sh"
echo ""
echo "Pour configurer un nom de domaine et HTTPS:"
echo "sudo /opt/challenge-convention/scripts/setup-domain.sh votre-domaine.com"
