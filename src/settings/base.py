"""
Contains all configurations for the project.
Should NOT contain any secrets.

>>> import src.settings as stg
>>> stg.COL_NAME
"""

import os

from src.settings.column_names import *

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
TRAINING_DATA_DIR = os.path.join(REPO_DIR, "data/training/")
PREDICTION_DATA_DIR = os.path.join(REPO_DIR, "data/prediction/")
OUTPUTS_DIR = os.path.join(REPO_DIR, "outputs")
MODEL_DIR = os.path.join(REPO_DIR, "src/domain/")

CATEGORY_MIN_THRESHOLD = 10

FEATURES_TO_KEEP = [
    ID_CLIENT_COL,
    ORIGINE_LEAD_COL,
    SOURCE_LEAD_COL,
    CONTACT_PAR_MAIL_COL,
    STATUT_ACTUEL_COL,
    CONVERTI_COL,
    NB_VISITES_COL,
    DUREE_SUR_SITEWEB_COL,
    DERNIERE_ACTIVITE_COL,
    SPECIALISATION_COL,
    COMMENT_ENTENDU_PARLER_COL,
    SOUHAITE_LIVRE_BLANC_COL,
]

SEED_TRAIN_TEST = 42

SEED_RF = 42

PROJECT_DESCRIPTION = "Projection desciption"
