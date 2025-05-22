from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime

db = SQLAlchemy()

class Participant(db.Model):
    """Modèle pour les participants au challenge."""
    
    __tablename__ = 'participants'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    franchise = Column(String(100), nullable=False)
    instagram_id = Column(String(100), nullable=True)
    linkedin_id = Column(String(255), nullable=True)
    date_inscription = Column(DateTime, default=datetime.utcnow)
    valide = Column(Boolean, default=False)
    
    def __init__(self, nom, email, franchise, instagram_id=None, linkedin_id=None):
        self.nom = nom
        self.email = email
        self.franchise = franchise
        self.instagram_id = instagram_id
        self.linkedin_id = linkedin_id
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email,
            'franchise': self.franchise,
            'instagram_id': self.instagram_id,
            'linkedin_id': self.linkedin_id,
            'date_inscription': self.date_inscription.isoformat() if self.date_inscription else None,
            'valide': self.valide
        }
