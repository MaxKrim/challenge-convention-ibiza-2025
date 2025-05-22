from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from functools import wraps
import os

admin_bp = Blueprint('admin', __name__)

# Configuration de l'authentification simple
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'challenge2025')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Page de connexion à l'interface d'administration."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.dashboard_admin'))
        else:
            flash('Identifiants incorrects. Veuillez réessayer.', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/admin/logout')
def logout():
    """Déconnexion de l'interface d'administration."""
    session.pop('admin_logged_in', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin')
@login_required
def index():
    """Page d'accueil de l'administration."""
    return redirect(url_for('dashboard.dashboard_admin'))

@admin_bp.route('/admin/parametres')
@login_required
def parametres():
    """Page de paramètres de l'application."""
    return render_template('admin/parametres.html')

@admin_bp.route('/admin/parametres/update', methods=['POST'])
@login_required
def update_parametres():
    """Met à jour les paramètres de l'application."""
    try:
        # Dans une version réelle, cette fonction mettrait à jour les paramètres
        flash('Paramètres mis à jour avec succès.', 'success')
    except Exception as e:
        flash(f'Erreur lors de la mise à jour des paramètres : {str(e)}', 'error')
    
    return redirect(url_for('admin.parametres'))
