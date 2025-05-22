from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.models import db, Participant
import qrcode
from io import BytesIO
import base64
import os

inscription_bp = Blueprint('inscription', __name__)

@inscription_bp.route('/inscription', methods=['GET'])
def formulaire_inscription():
    """Affiche le formulaire d'inscription."""
    return render_template('inscription/formulaire.html')

@inscription_bp.route('/inscription', methods=['POST'])
def traiter_inscription():
    """Traite le formulaire d'inscription."""
    try:
        # Récupération des données du formulaire
        nom = request.form.get('nom')
        email = request.form.get('email')
        franchise = request.form.get('franchise')
        instagram_id = request.form.get('instagram_id')
        linkedin_id = request.form.get('linkedin_id')
        
        # Validation des données
        if not nom or not email or not franchise:
            flash('Veuillez remplir tous les champs obligatoires.', 'error')
            return redirect(url_for('inscription.formulaire_inscription'))
        
        # Vérification si l'email existe déjà
        participant_existant = Participant.query.filter_by(email=email).first()
        if participant_existant:
            flash('Un participant avec cet email existe déjà.', 'error')
            return redirect(url_for('inscription.formulaire_inscription'))
        
        # Création du nouveau participant
        nouveau_participant = Participant(
            nom=nom,
            email=email,
            franchise=franchise,
            instagram_id=instagram_id,
            linkedin_id=linkedin_id
        )
        
        # Ajout à la base de données
        db.session.add(nouveau_participant)
        db.session.commit()
        
        flash('Inscription réussie ! Merci de votre participation.', 'success')
        return redirect(url_for('inscription.confirmation', participant_id=nouveau_participant.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Une erreur est survenue lors de l\'inscription : {str(e)}', 'error')
        return redirect(url_for('inscription.formulaire_inscription'))

@inscription_bp.route('/confirmation/<int:participant_id>')
def confirmation(participant_id):
    """Affiche la page de confirmation d'inscription."""
    participant = Participant.query.get_or_404(participant_id)
    return render_template('inscription/confirmation.html', participant=participant)

@inscription_bp.route('/qrcode')
def generer_qrcode():
    """Génère un QR code pour l'inscription."""
    # URL de base pour l'inscription (à adapter selon le déploiement)
    base_url = request.host_url.rstrip('/')
    inscription_url = f"{base_url}/inscription"
    
    # Génération du QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(inscription_url)
    qr.make(fit=True)
    
    # Création de l'image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Sauvegarde de l'image
    img_path = os.path.join('src', 'static', 'img', 'qrcode_inscription.png')
    img.save(img_path)
    
    # Conversion en base64 pour l'affichage
    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('inscription/qrcode.html', img_data=img_str, inscription_url=inscription_url)

@inscription_bp.route('/liste_participants')
def liste_participants():
    """Affiche la liste des participants (réservé à l'administration)."""
    participants = Participant.query.all()
    return render_template('admin/liste_participants.html', participants=participants)

@inscription_bp.route('/valider_participant/<int:participant_id>', methods=['POST'])
def valider_participant(participant_id):
    """Valide un participant."""
    participant = Participant.query.get_or_404(participant_id)
    participant.valide = True
    db.session.commit()
    flash(f'Le participant {participant.nom} a été validé.', 'success')
    return redirect(url_for('inscription.liste_participants'))
