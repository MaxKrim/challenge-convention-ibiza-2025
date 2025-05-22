# Guide d'installation et d'utilisation sur VPS

Ce guide détaille les étapes pour installer et utiliser l'application de suivi des publications réseaux sociaux pour le Challenge Convention Ibiza 2025 sur un VPS.

## Table des matières

1. [Prérequis](#1-prérequis)
2. [Location d'un VPS](#2-location-dun-vps)
3. [Installation de l'application](#3-installation-de-lapplication)
4. [Configuration](#4-configuration)
5. [Démarrage de l'application](#5-démarrage-de-lapplication)
6. [Utilisation](#6-utilisation)
7. [Maintenance](#7-maintenance)
8. [Résolution des problèmes courants](#8-résolution-des-problèmes-courants)

## 1. Prérequis

Pour utiliser cette application, vous aurez besoin de :

- Un VPS (serveur privé virtuel) avec au moins 1 Go de RAM et 20 Go d'espace disque
- Un nom de domaine (optionnel mais recommandé)
- Un navigateur web moderne pour accéder à l'application

Aucune connaissance en programmation n'est nécessaire pour l'installation et l'utilisation.

## 2. Location d'un VPS

### 2.1 Choix du fournisseur

Plusieurs fournisseurs proposent des VPS à partir de 5€/mois. Voici quelques options recommandées :

- [OVH](https://www.ovhcloud.com/fr/vps/) - VPS à partir de 3,99€/mois
- [Scaleway](https://www.scaleway.com/fr/virtual-instances/) - Instances à partir de 4€/mois
- [DigitalOcean](https://www.digitalocean.com/) - Droplets à partir de $5/mois
- [Hetzner](https://www.hetzner.com/cloud) - Cloud servers à partir de 4,15€/mois

### 2.2 Processus de location

1. Créez un compte chez le fournisseur de votre choix
2. Sélectionnez un VPS avec les caractéristiques minimales suivantes :
   - 1 vCPU
   - 1 Go de RAM
   - 20 Go de stockage SSD
   - Ubuntu 22.04 LTS comme système d'exploitation
3. Procédez au paiement (généralement par carte bancaire)
4. Notez les informations d'accès fournies par email :
   - Adresse IP du serveur
   - Nom d'utilisateur (généralement "root")
   - Mot de passe initial ou clé SSH

## 3. Installation de l'application

Pour simplifier l'installation, nous avons préparé un script automatique. Voici comment procéder :

### 3.1 Connexion au VPS

#### Sur Windows :
1. Téléchargez et installez [PuTTY](https://www.putty.org/)
2. Lancez PuTTY
3. Dans le champ "Host Name", entrez l'adresse IP de votre VPS
4. Cliquez sur "Open"
5. Acceptez l'alerte de sécurité si elle apparaît
6. Connectez-vous avec le nom d'utilisateur et le mot de passe fournis

#### Sur Mac ou Linux :
1. Ouvrez Terminal
2. Tapez la commande : `ssh root@ADRESSE_IP` (remplacez ADRESSE_IP par l'IP de votre VPS)
3. Acceptez l'alerte de sécurité en tapant "yes"
4. Entrez le mot de passe fourni

### 3.2 Installation automatique

Une fois connecté au VPS, exécutez les commandes suivantes :

```bash
# Téléchargement du script d'installation
wget https://raw.githubusercontent.com/votre-compte/challenge-convention/main/scripts/install.sh

# Attribution des droits d'exécution
chmod +x install.sh

# Exécution du script d'installation
./install.sh
```

Le script effectuera automatiquement les opérations suivantes :
- Mise à jour du système
- Installation des dépendances nécessaires (Python, Nginx, etc.)
- Téléchargement de l'application
- Configuration de la base de données
- Configuration du serveur web
- Mise en place des certificats SSL
- Démarrage de l'application

L'installation prend environ 5-10 minutes. À la fin, le script affichera l'URL à laquelle vous pourrez accéder à l'application.

## 4. Configuration

### 4.1 Configuration de base

La configuration de base est effectuée automatiquement par le script d'installation. Cependant, vous pouvez modifier certains paramètres en éditant le fichier de configuration :

```bash
nano /opt/challenge-convention/config.env
```

Paramètres importants :
- `ADMIN_USERNAME` : nom d'utilisateur pour l'interface d'administration
- `ADMIN_PASSWORD` : mot de passe pour l'interface d'administration
- `SECRET_KEY` : clé de sécurité pour l'application (ne pas modifier sauf si nécessaire)

Après modification, redémarrez l'application :

```bash
sudo systemctl restart challenge-convention
```

### 4.2 Configuration du nom de domaine (optionnel)

Si vous disposez d'un nom de domaine, vous pouvez l'utiliser pour accéder à l'application :

1. Chez votre registrar, créez un enregistrement DNS de type A pointant vers l'adresse IP de votre VPS
2. Exécutez la commande suivante sur votre VPS :
   ```bash
   sudo /opt/challenge-convention/scripts/setup-domain.sh votre-domaine.com
   ```
3. Le script configurera automatiquement Nginx et Let's Encrypt pour votre domaine

## 5. Démarrage de l'application

L'application démarre automatiquement après l'installation et à chaque redémarrage du VPS.

Pour vérifier l'état de l'application :

```bash
sudo systemctl status challenge-convention
```

Pour redémarrer l'application :

```bash
sudo systemctl restart challenge-convention
```

## 6. Utilisation

### 6.1 Accès à l'application

Accédez à l'application en ouvrant un navigateur web et en visitant :
- `http://ADRESSE_IP` (si vous n'avez pas configuré de nom de domaine)
- `https://votre-domaine.com` (si vous avez configuré un nom de domaine)

### 6.2 Interface d'administration

Pour accéder à l'interface d'administration :
1. Visitez `http://ADRESSE_IP/admin` ou `https://votre-domaine.com/admin`
2. Connectez-vous avec les identifiants configurés (par défaut : admin / challenge2025)

### 6.3 Génération du QR code d'inscription

1. Connectez-vous à l'interface d'administration
2. Allez dans la section "Inscription"
3. Cliquez sur "Générer QR Code"
4. Téléchargez l'image du QR code pour l'imprimer ou l'inclure dans vos communications

### 6.4 Collecte des publications

La collecte des publications est automatisée et s'exécute toutes les 30 minutes. Vous pouvez également lancer une collecte manuelle :

1. Connectez-vous à l'interface d'administration
2. Allez dans la section "Collecte"
3. Cliquez sur "Lancer la collecte"

### 6.5 Modération et scoring

1. Connectez-vous à l'interface d'administration
2. Allez dans la section "Modération"
3. Validez ou rejetez les publications
4. Attribuez des bonus d'originalité si nécessaire
5. Cliquez sur "Calculer les scores" pour mettre à jour le classement

### 6.6 Affichage du dashboard sur écran

Pour afficher le dashboard sur un écran pendant la convention :

1. Connectez un ordinateur à l'écran
2. Ouvrez un navigateur en mode plein écran (F11)
3. Visitez `http://ADRESSE_IP/dashboard/ecran` ou `https://votre-domaine.com/dashboard/ecran`
4. Le dashboard s'actualisera automatiquement toutes les 60 secondes

## 7. Maintenance

### 7.1 Sauvegardes

Des sauvegardes automatiques sont effectuées quotidiennement. Pour restaurer une sauvegarde :

```bash
sudo /opt/challenge-convention/scripts/restore-backup.sh YYYY-MM-DD
```

Remplacez `YYYY-MM-DD` par la date de la sauvegarde à restaurer.

### 7.2 Mises à jour

Si des mises à jour sont disponibles, exécutez :

```bash
sudo /opt/challenge-convention/scripts/update.sh
```

### 7.3 Logs

Pour consulter les logs de l'application :

```bash
sudo journalctl -u challenge-convention -f
```

## 8. Résolution des problèmes courants

### 8.1 L'application ne répond pas

1. Vérifiez l'état du service :
   ```bash
   sudo systemctl status challenge-convention
   ```

2. Si le service est arrêté, démarrez-le :
   ```bash
   sudo systemctl start challenge-convention
   ```

3. Vérifiez les logs pour identifier le problème :
   ```bash
   sudo journalctl -u challenge-convention -n 50
   ```

### 8.2 Problèmes de collecte des publications

Si la collecte des publications ne fonctionne pas correctement :

1. Vérifiez que les identifiants Instagram et LinkedIn des participants sont correctement formatés
2. Assurez-vous que les publications contiennent bien les mentions requises (@bhgroupefrance, @GroupeBHFrance)
3. Vérifiez les logs de collecte :
   ```bash
   sudo cat /opt/challenge-convention/logs/collecte.log
   ```

### 8.3 Réinitialisation du mot de passe administrateur

Si vous avez oublié le mot de passe administrateur :

```bash
sudo /opt/challenge-convention/scripts/reset-admin-password.sh
```

Le script vous demandera de saisir un nouveau mot de passe.

---

Pour toute assistance supplémentaire, contactez le support technique à l'adresse email fournie avec l'application.
