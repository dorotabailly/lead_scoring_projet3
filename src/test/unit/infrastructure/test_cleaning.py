"""
Unit tests for the script src/infrastructure/cleaning.py
"""

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

import src.settings.base as stg
from src.infrastructure.cleaning import InfraCleaner

json_input = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "Formulaire Lead Add",
        "SOURCE_LEAD": "Olark Chat",
        "NIVEAU_LEAD": "Select",
        "QUALITE_LEAD": "",
        "CONTACT_PAR_MAIL": "Non",
        "CONTACT_PAR_TELEPHONE": "Non",
        "STATUT_ACTUEL": "Sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "NB_PAGES_VUES_PAR_VISITE": 0,
        "DERNIERE_ACTIVITE": "Email ouvert",
        "DERNIERE_ACTIVITE_NOTABLE": "Email ouvert",
        "PAYS": "",
        "VILLE": "Select",
        "SPECIALISATION": "Marketing Management",
        "TAGS": "",
        "INDEX_ACTIVITE": "",
        "INDEX_PROFIL": "",
        "SCORE_ACTIVITE": "",
        "SCORE_PROFIL": "",
        "ANNONCE_VUE": "Non",
        "MAGAZINE": "Non",
        "ARTICLE_JOURNAL": "Non",
        "FORUM": "Non",
        "JOURNAUX": "Non",
        "PUB_DIGITALE": "Non",
        "RECOMMANDATION": "Non",
        "Comment avez-vous entendu parler de nous ?": "Select",
        "Souhaites-tu recevoir plus d'infos sur notre cours ?": "Non",
        "Souhaites-tu recevoir des mises à jour sur nos programmes ?": "Non",
        "Souhaites-tu recevoir des mises à jour par message privé ?": "Non",
        "Souhaites-tu payer par chèque ?": "Non",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "Non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "Soumission landing page",
        "SOURCE_LEAD": "Organic Search",
        "NIVEAU_LEAD": "Autre leads",
        "QUALITE_LEAD": "Pas du tout pertinent",
        "CONTACT_PAR_MAIL": "Non",
        "CONTACT_PAR_TELEPHONE": "Non",
        "STATUT_ACTUEL": "Sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 3,
        "DUREE_SUR_SITEWEB": 519,
        "NB_PAGES_VUES_PAR_VISITE": 3,
        "DERNIERE_ACTIVITE": "Page visitée sur le site",
        "DERNIERE_ACTIVITE_NOTABLE": "Modifié",
        "PAYS": "India",
        "VILLE": "Autres villes de Maharashtra",
        "SPECIALISATION": "Banking, Investment And Insurance",
        "TAGS": "Ne pas suivre de formation continue",
        "INDEX_ACTIVITE": "Moyen",
        "INDEX_PROFIL": "Elevé",
        "SCORE_ACTIVITE": 15,
        "SCORE_PROFIL": 17,
        "ANNONCE_VUE": "Non",
        "MAGAZINE": "Non",
        "ARTICLE_JOURNAL": "Non",
        "FORUM": "Non",
        "JOURNAUX": "Non",
        "PUB_DIGITALE": "Non",
        "RECOMMANDATION": "Non",
        "Comment avez-vous entendu parler de nous ?": "Select",
        "Souhaites-tu recevoir plus d'infos sur notre cours ?": "Non",
        "Souhaites-tu recevoir des mises à jour sur nos programmes ?": "Non",
        "Souhaites-tu recevoir des mises à jour par message privé ?": "Non",
        "Souhaites-tu payer par chèque ?": "Non",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "Oui",
    },
]


features_to_keep = [
    "ID_CLIENT",
    "ORIGINE_LEAD",
    "SOURCE_LEAD",
    "CONTACT_PAR_MAIL",
    "STATUT_ACTUEL",
    "CONVERTI",
    "NB_VISITES",
    "DUREE_SUR_SITEWEB",
    "DERNIERE_ACTIVITE",
    "SPECIALISATION",
    "Comment avez-vous entendu parler de nous ?",
    "Souhaites-tu recevoir une copie de notre livre blanc ?",
]


json_output_accent = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "Formulaire Lead Add",
        "SOURCE_LEAD": "Olark Chat",
        "CONTACT_PAR_MAIL": "Non",
        "STATUT_ACTUEL": "Sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "Email ouvert",
        "SPECIALISATION": "Marketing Management",
        "Comment avez-vous entendu parler de nous ?": "Select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "Non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "Soumission landing page",
        "SOURCE_LEAD": "Organic Search",
        "CONTACT_PAR_MAIL": "Non",
        "STATUT_ACTUEL": "Sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 3,
        "DUREE_SUR_SITEWEB": 519,
        "DERNIERE_ACTIVITE": "Page visitee sur le site",
        "SPECIALISATION": "Banking, Investment And Insurance",
        "Comment avez-vous entendu parler de nous ?": "Select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "Oui",
    },
]


json_output_upper_case = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "formulaire lead add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "soumission landing page",
        "SOURCE_LEAD": "organic search",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 3,
        "DUREE_SUR_SITEWEB": 519,
        "DERNIERE_ACTIVITE": "page visitée sur le site",
        "SPECIALISATION": "banking, investment and insurance",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "oui",
    },
]


json_output_transformer = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "formulaire lead add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "soumission landing page",
        "SOURCE_LEAD": "organic search",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "sans emploi",
        "CONVERTI": 0,
        "NB_VISITES": 3,
        "DUREE_SUR_SITEWEB": 519,
        "DERNIERE_ACTIVITE": "page visitee sur le site",
        "SPECIALISATION": "banking, investment and insurance",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "oui",
    },
]

df_input = pd.DataFrame(json_input)


df_output_accent = pd.DataFrame(json_output_accent)
df_output_upper_case = pd.DataFrame(json_output_upper_case)

df_output_change_cat = df_output_accent.copy()
categorial_cols = df_output_change_cat.select_dtypes(include=object).columns
for col in categorial_cols:
    df_output_change_cat[col] = df_output_change_cat[col].astype("category")

df_output_transformer = pd.DataFrame(json_output_transformer)
categorial_cols = df_output_transformer.select_dtypes(include=object).columns
for col in categorial_cols:
    df_output_transformer[col] = df_output_transformer[col].astype("category")
df_output_transformer = df_output_transformer.set_index(stg.ID_CLIENT_COL)

columns_names_input = df_input.columns.to_list()


def test_select_features():
    tr = InfraCleaner()
    df_tr = tr._select_features(df_input)
    columns_output = df_tr.columns.to_list()
    assert set(features_to_keep) == set(columns_output)


def test_remove_accent():
    tr = InfraCleaner()
    df_tr = tr._select_features(df_input)
    df_tr = tr._remove_accents(df_tr)
    assert_frame_equal(df_tr, df_output_accent)


def test_remove_upper_case():
    tr = InfraCleaner()
    df_tr = tr._select_features(df_input)
    df_tr = tr._remove_upper_case(df_tr)
    assert_frame_equal(df_tr, df_output_upper_case)


def test_change_object_type_to_category():
    tr = InfraCleaner()
    df_tr = tr._select_features(df_input)
    df_tr = tr._remove_accents(df_tr)
    df_tr = tr._change_object_type_to_category(df_tr)
    assert_series_equal(df_tr.dtypes, df_output_change_cat.dtypes)


def test_change_object_type_to_category():
    tr = InfraCleaner()
    df_tr = tr._select_features(df_input)
    df_tr = tr._remove_accents(df_tr)
    df_tr = tr._change_object_type_to_category(df_tr)
    assert_series_equal(df_tr.dtypes, df_output_change_cat.dtypes)


def test_transform():
    tr = InfraCleaner()
    df_tr = tr.transform(df_input)
    assert_frame_equal(df_tr, df_output_transformer)


def test_fit():
    tr = InfraCleaner()
    tr2 = tr.fit(df_input)
    assert tr == tr2


def test_fit_transform():
    tr = InfraCleaner()
    df_tr = tr.fit_transform(df_input)
    assert_frame_equal(df_tr, df_output_transformer)


test_fit_transform()
