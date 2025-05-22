from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models import db, Participant, Publication, Score, ClassementFinal
import os

# Création des blueprints
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    """Page d'accueil du site."""
    return render_template('index.html')

@routes_bp.route('/regles')
def regles():
    """Page des règles du challenge."""
    return render_template('regles.html')

@routes_bp.route('/contact')
def contact():
    """Page de contact."""
    return render_template('contact.html')

@routes_bp.route('/resultats')
def resultats():
    """Page des résultats finaux."""
    # Récupération du classement complet
    classement = ClassementFinal.query.join(Participant).order_by(ClassementFinal.score_final.desc()).all()
    
    return render_template('resultats.html', classement=classement)
