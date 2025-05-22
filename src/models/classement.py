from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class ClassementFinal(db.Model):
    """Modèle pour le classement final des participants."""
    
    __tablename__ = 'classement_final'
    
    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey('participants.id'), nullable=False)
    nombre_publications = Column(Integer, default=0)
    score_cumule = Column(Integer, default=0)
    multiplicateur = Column(Float, default=1.0)
    score_final = Column(Float, default=0.0)
    
    # Relation avec le participant
    participant = relationship("Participant", backref="classement")
    
    def __init__(self, participant_id, nombre_publications=0, score_cumule=0):
        self.participant_id = participant_id
        self.nombre_publications = nombre_publications
        self.score_cumule = score_cumule
        self.calculer_multiplicateur()
        self.calculer_score_final()
        
    def calculer_multiplicateur(self):
        """Calcule le multiplicateur de fréquence (bonus de 5% par publication supplémentaire, plafonné à 50%)."""
        if self.nombre_publications <= 1:
            self.multiplicateur = 1.0
        else:
            # Formule: 1 + (nombre_publications - 1) * 0.05, plafonné à 1.5
            self.multiplicateur = min(1.5, 1 + (self.nombre_publications - 1) * 0.05)
        
    def calculer_score_final(self):
        """Calcule le score final en appliquant le multiplicateur au score cumulé."""
        self.score_final = self.score_cumule * self.multiplicateur
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'nombre_publications': self.nombre_publications,
            'score_cumule': self.score_cumule,
            'multiplicateur': self.multiplicateur,
            'score_final': self.score_final
        }
