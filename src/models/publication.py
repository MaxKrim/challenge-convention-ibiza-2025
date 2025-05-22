from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Publication(db.Model):
    """Modèle pour les publications des réseaux sociaux."""
    
    __tablename__ = 'publications'
    
    id = Column(Integer, primary_key=True)
    plateforme = Column(String(20), nullable=False)  # 'Instagram' ou 'LinkedIn'
    url = Column(String(255), nullable=False, unique=True)
    auteur_id = Column(String(100), nullable=False)
    participant_id = Column(Integer, ForeignKey('participants.id'), nullable=True)
    date_publication = Column(DateTime, nullable=False)
    likes = Column(Integer, default=0)
    commentaires = Column(Integer, default=0)
    partages = Column(Integer, default=0)
    contenu = Column(Text, nullable=True)
    valide = Column(Boolean, default=False)
    
    # Relation avec le participant
    participant = relationship("Participant", backref="publications")
    
    def __init__(self, plateforme, url, auteur_id, date_publication, 
                 likes=0, commentaires=0, partages=0, contenu=None, participant_id=None):
        self.plateforme = plateforme
        self.url = url
        self.auteur_id = auteur_id
        self.date_publication = date_publication
        self.likes = likes
        self.commentaires = commentaires
        self.partages = partages
        self.contenu = contenu
        self.participant_id = participant_id
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'plateforme': self.plateforme,
            'url': self.url,
            'auteur_id': self.auteur_id,
            'participant_id': self.participant_id,
            'date_publication': self.date_publication.isoformat() if self.date_publication else None,
            'likes': self.likes,
            'commentaires': self.commentaires,
            'partages': self.partages,
            'contenu': self.contenu,
            'valide': self.valide
        }
