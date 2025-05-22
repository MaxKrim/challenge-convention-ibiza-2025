from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Score(db.Model):
    """Modèle pour les scores des publications."""
    
    __tablename__ = 'scores'
    
    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey('participants.id'), nullable=False)
    publication_id = Column(Integer, ForeignKey('publications.id'), nullable=False)
    points_base = Column(Integer, default=10)  # 10 points de base par publication
    points_likes = Column(Integer, default=0)  # 1 point par like/réaction
    points_commentaires = Column(Integer, default=0)  # 2 points par commentaire
    points_partages = Column(Integer, default=0)  # 3 points par partage
    bonus_originalite = Column(Integer, default=0)  # 0-20 points, attribution manuelle
    score_total = Column(Integer, default=0)  # Somme des points
    date_calcul = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    participant = relationship("Participant", backref="scores")
    publication = relationship("Publication", backref="score")
    
    def __init__(self, participant_id, publication_id, points_base=10, 
                 points_likes=0, points_commentaires=0, points_partages=0, 
                 bonus_originalite=0):
        self.participant_id = participant_id
        self.publication_id = publication_id
        self.points_base = points_base
        self.points_likes = points_likes
        self.points_commentaires = points_commentaires
        self.points_partages = points_partages
        self.bonus_originalite = bonus_originalite
        self.calculer_score_total()
        
    def calculer_score_total(self):
        """Calcule le score total en additionnant tous les points."""
        self.score_total = (self.points_base + 
                           self.points_likes + 
                           self.points_commentaires + 
                           self.points_partages + 
                           self.bonus_originalite)
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'publication_id': self.publication_id,
            'points_base': self.points_base,
            'points_likes': self.points_likes,
            'points_commentaires': self.points_commentaires,
            'points_partages': self.points_partages,
            'bonus_originalite': self.bonus_originalite,
            'score_total': self.score_total,
            'date_calcul': self.date_calcul.isoformat() if self.date_calcul else None
        }
