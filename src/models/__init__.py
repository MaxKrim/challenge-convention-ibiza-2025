from src.models.participant import db as participant_db
from src.models.publication import db as publication_db
from src.models.score import db as score_db
from src.models.classement import db as classement_db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import des modèles pour les rendre disponibles
from src.models.participant import Participant
from src.models.publication import Publication
from src.models.score import Score
from src.models.classement import ClassementFinal
