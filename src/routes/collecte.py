from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.models import db, Publication, Participant
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import random
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

collecte_bp = Blueprint('collecte', __name__)

@collecte_bp.route('/collecte/dashboard')
def dashboard_collecte():
    """Affiche le dashboard de collecte des publications."""
    publications_instagram = Publication.query.filter_by(plateforme='Instagram').order_by(Publication.date_publication.desc()).all()
    publications_linkedin = Publication.query.filter_by(plateforme='LinkedIn').order_by(Publication.date_publication.desc()).all()
    
    return render_template('admin/collecte_dashboard.html', 
                          publications_instagram=publications_instagram,
                          publications_linkedin=publications_linkedin)

@collecte_bp.route('/collecte/lancer', methods=['POST'])
def lancer_collecte():
    """Lance manuellement la collecte des publications."""
    try:
        # Récupération des paramètres
        plateforme = request.form.get('plateforme', 'all')
        
        if plateforme == 'instagram' or plateforme == 'all':
            collecter_publications_instagram()
        
        if plateforme == 'linkedin' or plateforme == 'all':
            collecter_publications_linkedin()
        
        flash('Collecte des publications lancée avec succès.', 'success')
    except Exception as e:
        flash(f'Erreur lors de la collecte des publications : {str(e)}', 'error')
    
    return redirect(url_for('collecte.dashboard_collecte'))

def collecter_publications_instagram():
    """Collecte les publications Instagram mentionnant @bhgroupefrance."""
    logger.info("Début de la collecte des publications Instagram")
    
    # Liste des participants avec un compte Instagram
    participants = Participant.query.filter(Participant.instagram_id.isnot(None)).all()
    
    for participant in participants:
        try:
            # Nettoyage de l'identifiant Instagram (suppression du @ si présent)
            instagram_id = participant.instagram_id.strip().lstrip('@')
            
            # Simulation de collecte (dans une version réelle, utiliserait un scraping plus avancé)
            # Cette fonction simule la collecte pour éviter les problèmes légaux et techniques du scraping
            publications = simuler_collecte_instagram(instagram_id)
            
            for pub_data in publications:
                # Vérification si la publication existe déjà
                pub_existante = Publication.query.filter_by(url=pub_data['url']).first()
                if not pub_existante:
                    # Création d'une nouvelle publication
                    nouvelle_pub = Publication(
                        plateforme='Instagram',
                        url=pub_data['url'],
                        auteur_id=instagram_id,
                        participant_id=participant.id,
                        date_publication=pub_data['date'],
                        likes=pub_data['likes'],
                        commentaires=pub_data['commentaires'],
                        contenu=pub_data['contenu']
                    )
                    db.session.add(nouvelle_pub)
            
            db.session.commit()
            logger.info(f"Publications collectées pour {instagram_id}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur lors de la collecte pour {participant.instagram_id}: {str(e)}")
    
    logger.info("Fin de la collecte des publications Instagram")

def collecter_publications_linkedin():
    """Collecte les publications LinkedIn mentionnant @GroupeBHFrance."""
    logger.info("Début de la collecte des publications LinkedIn")
    
    # Liste des participants avec un compte LinkedIn
    participants = Participant.query.filter(Participant.linkedin_id.isnot(None)).all()
    
    for participant in participants:
        try:
            # Extraction de l'identifiant LinkedIn
            linkedin_id = participant.linkedin_id
            
            # Simulation de collecte (dans une version réelle, utiliserait un scraping plus avancé)
            publications = simuler_collecte_linkedin(linkedin_id)
            
            for pub_data in publications:
                # Vérification si la publication existe déjà
                pub_existante = Publication.query.filter_by(url=pub_data['url']).first()
                if not pub_existante:
                    # Création d'une nouvelle publication
                    nouvelle_pub = Publication(
                        plateforme='LinkedIn',
                        url=pub_data['url'],
                        auteur_id=linkedin_id,
                        participant_id=participant.id,
                        date_publication=pub_data['date'],
                        likes=pub_data['likes'],
                        commentaires=pub_data['commentaires'],
                        partages=pub_data['partages'],
                        contenu=pub_data['contenu']
                    )
                    db.session.add(nouvelle_pub)
            
            db.session.commit()
            logger.info(f"Publications collectées pour {linkedin_id}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur lors de la collecte pour {participant.linkedin_id}: {str(e)}")
    
    logger.info("Fin de la collecte des publications LinkedIn")

def simuler_collecte_instagram(instagram_id):
    """
    Simule la collecte de publications Instagram pour éviter les problèmes légaux et techniques.
    Dans une version réelle, cette fonction serait remplacée par un scraping réel.
    """
    # Simulation de 1 à 3 publications par utilisateur
    nombre_publications = random.randint(1, 3)
    publications = []
    
    for i in range(nombre_publications):
        # Date aléatoire dans les 3 derniers jours
        jours_aleatoires = random.randint(0, 2)
        heures_aleatoires = random.randint(0, 23)
        minutes_aleatoires = random.randint(0, 59)
        date_publication = datetime.now() - timedelta(days=jours_aleatoires, hours=heures_aleatoires, minutes=minutes_aleatoires)
        
        # Données simulées
        publication = {
            'url': f"https://instagram.com/p/{instagram_id}_{i}_{int(time.time())}",
            'date': date_publication,
            'likes': random.randint(5, 100),
            'commentaires': random.randint(0, 20),
            'contenu': f"Belle journée à la convention Ibiza avec @bhgroupefrance! #{i+1} #convention #ibiza"
        }
        
        publications.append(publication)
    
    return publications

def simuler_collecte_linkedin(linkedin_id):
    """
    Simule la collecte de publications LinkedIn pour éviter les problèmes légaux et techniques.
    Dans une version réelle, cette fonction serait remplacée par un scraping réel.
    """
    # Simulation de 1 à 2 publications par utilisateur
    nombre_publications = random.randint(1, 2)
    publications = []
    
    for i in range(nombre_publications):
        # Date aléatoire dans les 3 derniers jours
        jours_aleatoires = random.randint(0, 2)
        heures_aleatoires = random.randint(0, 23)
        minutes_aleatoires = random.randint(0, 59)
        date_publication = datetime.now() - timedelta(days=jours_aleatoires, hours=heures_aleatoires, minutes=minutes_aleatoires)
        
        # Données simulées
        publication = {
            'url': f"https://linkedin.com/posts/{linkedin_id}_{i}_{int(time.time())}",
            'date': date_publication,
            'likes': random.randint(10, 150),
            'commentaires': random.randint(0, 30),
            'partages': random.randint(0, 15),
            'contenu': f"Ravi de participer à la convention Ibiza 2025 avec @GroupeBHFrance! Une expérience incroyable. #{i+1} #networking #business"
        }
        
        publications.append(publication)
    
    return publications

@collecte_bp.route('/collecte/valider/<int:publication_id>', methods=['POST'])
def valider_publication(publication_id):
    """Valide une publication."""
    publication = Publication.query.get_or_404(publication_id)
    publication.valide = True
    db.session.commit()
    flash(f'La publication a été validée.', 'success')
    return redirect(url_for('collecte.dashboard_collecte'))

@collecte_bp.route('/collecte/rejeter/<int:publication_id>', methods=['POST'])
def rejeter_publication(publication_id):
    """Rejette une publication."""
    publication = Publication.query.get_or_404(publication_id)
    db.session.delete(publication)
    db.session.commit()
    flash(f'La publication a été rejetée et supprimée.', 'success')
    return redirect(url_for('collecte.dashboard_collecte'))
