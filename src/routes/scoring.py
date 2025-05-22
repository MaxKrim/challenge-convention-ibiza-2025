from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.models import db, Score, Publication, Participant, ClassementFinal
from datetime import datetime

scoring_bp = Blueprint('scoring', __name__)

@scoring_bp.route('/scoring/dashboard')
def dashboard_scoring():
    """Affiche le dashboard de scoring."""
    scores = Score.query.order_by(Score.date_calcul.desc()).all()
    classement = ClassementFinal.query.join(Participant).order_by(ClassementFinal.score_final.desc()).all()
    
    return render_template('admin/scoring_dashboard.html', 
                          scores=scores,
                          classement=classement)

@scoring_bp.route('/scoring/calculer', methods=['POST'])
def calculer_scores():
    """Lance le calcul des scores pour toutes les publications validées."""
    try:
        # Récupération des publications validées sans score
        publications = Publication.query.filter_by(valide=True).all()
        
        for publication in publications:
            # Vérification si un score existe déjà pour cette publication
            score_existant = Score.query.filter_by(publication_id=publication.id).first()
            
            if not score_existant:
                # Calcul des points selon les règles définies
                points_base = 10  # 10 points de base par publication
                points_likes = publication.likes * 1  # 1 point par like/réaction
                points_commentaires = publication.commentaires * 2  # 2 points par commentaire
                points_partages = publication.partages * 3 if publication.partages else 0  # 3 points par partage
                
                # Création du score
                nouveau_score = Score(
                    participant_id=publication.participant_id,
                    publication_id=publication.id,
                    points_base=points_base,
                    points_likes=points_likes,
                    points_commentaires=points_commentaires,
                    points_partages=points_partages,
                    bonus_originalite=0  # À attribuer manuellement
                )
                nouveau_score.calculer_score_total()
                db.session.add(nouveau_score)
        
        db.session.commit()
        
        # Mise à jour du classement final
        mettre_a_jour_classement()
        
        flash('Calcul des scores effectué avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors du calcul des scores : {str(e)}', 'error')
    
    return redirect(url_for('scoring.dashboard_scoring'))

@scoring_bp.route('/scoring/bonus/<int:score_id>', methods=['POST'])
def attribuer_bonus(score_id):
    """Attribue un bonus d'originalité à un score."""
    try:
        score = Score.query.get_or_404(score_id)
        bonus = int(request.form.get('bonus', 0))
        
        # Validation du bonus (entre 0 et 20)
        if bonus < 0 or bonus > 20:
            flash('Le bonus doit être compris entre 0 et 20 points.', 'error')
            return redirect(url_for('scoring.dashboard_scoring'))
        
        score.bonus_originalite = bonus
        score.calculer_score_total()
        db.session.commit()
        
        # Mise à jour du classement final
        mettre_a_jour_classement()
        
        flash(f'Bonus de {bonus} points attribué avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'attribution du bonus : {str(e)}', 'error')
    
    return redirect(url_for('scoring.dashboard_scoring'))

def mettre_a_jour_classement():
    """Met à jour le classement final des participants."""
    try:
        # Récupération de tous les participants
        participants = Participant.query.all()
        
        for participant in participants:
            # Récupération des scores du participant
            scores = Score.query.filter_by(participant_id=participant.id).all()
            
            if scores:
                # Calcul du nombre de publications et du score cumulé
                nombre_publications = len(scores)
                score_cumule = sum(score.score_total for score in scores)
                
                # Vérification si un classement existe déjà pour ce participant
                classement = ClassementFinal.query.filter_by(participant_id=participant.id).first()
                
                if classement:
                    # Mise à jour du classement existant
                    classement.nombre_publications = nombre_publications
                    classement.score_cumule = score_cumule
                    classement.calculer_multiplicateur()
                    classement.calculer_score_final()
                else:
                    # Création d'un nouveau classement
                    nouveau_classement = ClassementFinal(
                        participant_id=participant.id,
                        nombre_publications=nombre_publications,
                        score_cumule=score_cumule
                    )
                    db.session.add(nouveau_classement)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

@scoring_bp.route('/scoring/finaliser', methods=['POST'])
def finaliser_classement():
    """Finalise le classement pour l'annonce des résultats."""
    try:
        # Mise à jour du classement final
        mettre_a_jour_classement()
        
        flash('Classement final généré avec succès.', 'success')
    except Exception as e:
        flash(f'Erreur lors de la finalisation du classement : {str(e)}', 'error')
    
    return redirect(url_for('scoring.dashboard_scoring'))

@scoring_bp.route('/scoring/exporter', methods=['GET'])
def exporter_resultats():
    """Exporte les résultats au format CSV."""
    try:
        # Dans une version réelle, cette fonction générerait un fichier CSV
        # Pour l'instant, on redirige simplement vers le dashboard
        flash('Fonctionnalité d\'export en cours de développement.', 'info')
    except Exception as e:
        flash(f'Erreur lors de l\'export des résultats : {str(e)}', 'error')
    
    return redirect(url_for('scoring.dashboard_scoring'))
