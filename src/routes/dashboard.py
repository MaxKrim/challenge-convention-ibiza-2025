from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.models import db, Participant, Publication, Score, ClassementFinal
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def accueil():
    """Page d'accueil du challenge."""
    return render_template('dashboard/accueil.html')

@dashboard_bp.route('/dashboard/public')
def dashboard_public():
    """Affiche le dashboard public avec le classement des 10 meilleurs participants."""
    # Récupération du top 10 des participants
    top_participants = ClassementFinal.query.join(Participant).order_by(ClassementFinal.score_final.desc()).limit(10).all()
    
    # Récupération des meilleures publications (les 5 plus récentes validées)
    meilleures_publications = Publication.query.filter_by(valide=True).order_by(Publication.date_publication.desc()).limit(5).all()
    
    return render_template('dashboard/public.html', 
                          top_participants=top_participants,
                          meilleures_publications=meilleures_publications)

@dashboard_bp.route('/dashboard/ecran')
def dashboard_ecran():
    """Version du dashboard optimisée pour l'affichage sur grand écran."""
    # Récupération du top 10 des participants
    top_participants = ClassementFinal.query.join(Participant).order_by(ClassementFinal.score_final.desc()).limit(10).all()
    
    # Récupération des meilleures publications (les 3 plus récentes validées)
    meilleures_publications = Publication.query.filter_by(valide=True).order_by(Publication.date_publication.desc()).limit(3).all()
    
    return render_template('dashboard/ecran.html', 
                          top_participants=top_participants,
                          meilleures_publications=meilleures_publications)

@dashboard_bp.route('/dashboard/admin')
def dashboard_admin():
    """Dashboard d'administration principal."""
    # Statistiques générales
    nb_participants = Participant.query.count()
    nb_publications = Publication.query.count()
    nb_publications_validees = Publication.query.filter_by(valide=True).count()
    
    # Publications récentes à valider
    publications_a_valider = Publication.query.filter_by(valide=False).order_by(Publication.date_publication.desc()).limit(10).all()
    
    # Top 5 des participants
    top_participants = ClassementFinal.query.join(Participant).order_by(ClassementFinal.score_final.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          nb_participants=nb_participants,
                          nb_publications=nb_publications,
                          nb_publications_validees=nb_publications_validees,
                          publications_a_valider=publications_a_valider,
                          top_participants=top_participants)

@dashboard_bp.route('/api/classement')
def api_classement():
    """API pour récupérer le classement au format JSON."""
    classement = ClassementFinal.query.join(Participant).order_by(ClassementFinal.score_final.desc()).all()
    
    resultat = []
    for c in classement:
        participant = Participant.query.get(c.participant_id)
        resultat.append({
            'position': len(resultat) + 1,
            'nom': participant.nom,
            'franchise': participant.franchise,
            'nombre_publications': c.nombre_publications,
            'score_cumule': c.score_cumule,
            'multiplicateur': c.multiplicateur,
            'score_final': c.score_final
        })
    
    return jsonify(resultat)

@dashboard_bp.route('/api/publications')
def api_publications():
    """API pour récupérer les publications au format JSON."""
    publications = Publication.query.filter_by(valide=True).order_by(Publication.date_publication.desc()).all()
    
    resultat = []
    for p in publications:
        participant = Participant.query.get(p.participant_id)
        resultat.append({
            'id': p.id,
            'plateforme': p.plateforme,
            'url': p.url,
            'auteur': participant.nom if participant else "Inconnu",
            'date': p.date_publication.isoformat() if p.date_publication else None,
            'likes': p.likes,
            'commentaires': p.commentaires,
            'partages': p.partages,
            'contenu': p.contenu
        })
    
    return jsonify(resultat)
