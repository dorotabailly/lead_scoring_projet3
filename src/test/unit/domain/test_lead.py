"""
Unit tests for the script src/domain/lead.py
"""

import numpy as np
import pytest

import src.settings.base as stg
from src.domain.lead import Lead

"""

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
"""


json_lead_data1 = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "Formulaire Lead Add",
        "SOURCE_LEAD": "Olark Chat",
        "CONTACT_PAR_MAIL": "Non",
        "STATUT_ACTUEL": "Sans emploi",
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "Email ouvert",
        "SPECIALISATION": "Marketing Management",
        "Comment avez-vous entendu parler de nous ?": "Select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "Non",
    }
]

json_lead_data2 = [
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "Soumission landing page",
        "SOURCE_LEAD": "Organic Search",
        "CONTACT_PAR_MAIL": "Non",
        "STATUT_ACTUEL": "Sans emploi",
        "NB_VISITES": 3,
        "DUREE_SUR_SITEWEB": 519,
        "DERNIERE_ACTIVITE": "Email ouvert",
        "SPECIALISATION": "Banking, Investment And Insurance",
        "Comment avez-vous entendu parler de nous ?": "Select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "Oui",
    }
]


@pytest.mark.parametrize(
    "json_inputs,expected",
    [(json_lead_data1, 0.6844176750798613), (json_lead_data2, 0.5046263521481003)],
)
def test_lead(json_inputs, expected):

    result = Lead().predict(*json_inputs)
    result = result["result"]
    result = np.round(result, 16)

    assert result == expected  # Basic assertion
