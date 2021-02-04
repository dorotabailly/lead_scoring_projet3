"""
Unit tests for the script src/domain/features_eng.py
"""

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from sklearn.pipeline import make_pipeline, make_union

import src.settings.base as stg
from src.domain.features_eng import (
    AddFeatures,
    DomainCleaner,
    FeatureSelector,
    RegroupeCreateCategoryAutre,
)
from src.infrastructure.cleaning import InfraCleaner

json_input = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "formulaire lead add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "homme d'affaire",
        "CONVERTI": 0,
        "NB_VISITES": 100,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "formulaire quick add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "professionnel en activite",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
]

df_input = pd.DataFrame(json_input)
categorial_cols = df_input.select_dtypes(include=object).columns
for col in categorial_cols:
    df_input[col] = df_input[col].astype("category")
df_input = df_input.set_index(stg.ID_CLIENT_COL)

json_output_outliers = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "formulaire lead add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "homme d'affaire",
        "CONVERTI": 0,
        "NB_VISITES": np.nan,
        "DUREE_SUR_SITEWEB": np.nan,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "formulaire quick add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "professionnel en activite",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
]

df_output_outliers = pd.DataFrame(json_output_outliers)
categorial_cols = df_output_outliers.select_dtypes(include=object).columns
for col in categorial_cols:
    df_output_outliers[col] = df_output_outliers[col].astype("category")
df_output_outliers = df_output_outliers.set_index(stg.ID_CLIENT_COL)

json_output_values = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "formulaire add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "en activite",
        "CONVERTI": 0,
        "NB_VISITES": 100,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "formulaire add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "en activite",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
]

df_output_values = pd.DataFrame(json_output_values)
categorial_cols = df_output_values.select_dtypes(include=object).columns
for col in categorial_cols:
    df_output_values[col] = df_output_values[col].astype("category")
df_output_values = df_output_values.set_index(stg.ID_CLIENT_COL)

json_output_transformer = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "formulaire add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "en activite",
        "CONVERTI": 0,
        "NB_VISITES": np.nan,
        "DUREE_SUR_SITEWEB": np.nan,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "formulaire add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "en activite",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
    },
]

df_output_transformer = pd.DataFrame(json_output_transformer)
categorial_cols = df_output_transformer.select_dtypes(include=object).columns
for col in categorial_cols:
    df_output_transformer[col] = df_output_transformer[col].astype("category")
df_output_transformer = df_output_transformer.set_index(stg.ID_CLIENT_COL)


json_input_start = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "Formulaire Lead Add",
        "SOURCE_LEAD": "Olark Chat",
        "NIVEAU_LEAD": "Select",
        "QUALITE_LEAD": "",
        "CONTACT_PAR_MAIL": "Non",
        "CONTACT_PAR_TELEPHONE": "Non",
        "STATUT_ACTUEL": "Homme d'affaire",
        "CONVERTI": 0,
        "NB_VISITES": 100,
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
        "ORIGINE_LEAD": "Formulaire Quick Add",
        "SOURCE_LEAD": "Olark Chat",
        "NIVEAU_LEAD": "Select",
        "QUALITE_LEAD": "",
        "CONTACT_PAR_MAIL": "Non",
        "CONTACT_PAR_TELEPHONE": "Non",
        "STATUT_ACTUEL": "Professionnel en activite",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "NB_PAGES_VUES_PAR_VISITE": 3,
        "DERNIERE_ACTIVITE": "Email ouvert",
        "DERNIERE_ACTIVITE_NOTABLE": "Email ouvert",
        "PAYS": "",
        "VILLE": "Select",
        "SPECIALISATION": "Marketing Management",
        "TAGS": "",
        "INDEX_ACTIVITE": "",
        "INDEX_PROFIL": "",
        "SCORE_ACTIVITE": np.nan,
        "SCORE_PROFIL": np.nan,
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
]

df_input_start = pd.DataFrame(json_input_start)


json_output_addfeatures = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "formulaire add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "en activite",
        "CONVERTI": 0,
        "NB_VISITES": np.nan,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
        "NB_DUREE_MOY_PAR_VISITE": np.nan,
    },
    {
        "ID_CLIENT": 650444,
        "ORIGINE_LEAD": "formulaire add",
        "SOURCE_LEAD": "olark chat",
        "CONTACT_PAR_MAIL": "non",
        "STATUT_ACTUEL": "en activite",
        "CONVERTI": 0,
        "NB_VISITES": 0,
        "DERNIERE_ACTIVITE": "email ouvert",
        "SPECIALISATION": "marketing management",
        "Comment avez-vous entendu parler de nous ?": "select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "non",
        "NB_DUREE_MOY_PAR_VISITE": 0,
    },
]

df_output_addfeatures = pd.DataFrame(json_output_addfeatures)
categorial_cols = df_output_addfeatures.select_dtypes(include=object).columns
for col in categorial_cols:
    df_output_addfeatures[col] = df_output_addfeatures[col].astype("category")
df_output_addfeatures = df_output_addfeatures.set_index(stg.ID_CLIENT_COL)


df_output_select_numeric = df_output_addfeatures.select_dtypes(include=np.number)
df_output_select_category = df_output_addfeatures.select_dtypes(include="category")


df_output_regroup_categories = pd.DataFrame(
    {
        stg.ID_CLIENT_COL: [628707, 650444],
        stg.ORIGINE_LEAD_COL: ["autre", "autre"],
        stg.SOURCE_LEAD_COL: ["autre", "autre"],
        stg.CONTACT_PAR_MAIL_COL: ["autre", "autre"],
        stg.STATUT_ACTUEL_COL: ["autre", "autre"],
        stg.DERNIERE_ACTIVITE_COL: ["autre", "autre"],
        stg.SPECIALISATION_COL: ["autre", "autre"],
        stg.COMMENT_ENTENDU_PARLER_COL: ["autre", "autre"],
        stg.SOUHAITE_LIVRE_BLANC_COL: ["autre", "autre"],
    }
)

df_output_regroup_categories = df_output_regroup_categories.set_index(stg.ID_CLIENT_COL)
df_output_regroup_categories = df_output_regroup_categories.astype("category")


def test_correct_outliers_errors():
    tr = DomainCleaner()
    df_tr = tr._correct_outliers_errors(df_input)
    assert_frame_equal(df_tr, df_output_outliers)


def test_correct_values():
    tr = DomainCleaner()
    df_tr = tr._correct_values(df_input)
    assert_frame_equal(df_tr, df_output_values)


def test_transform():
    tr = DomainCleaner()
    df_tr = tr.transform(df_input)
    assert_frame_equal(df_tr, df_output_transformer)


def test_pipeline():

    my_pipeline = make_pipeline(InfraCleaner(), DomainCleaner())
    df_tr = my_pipeline.transform(df_input_start)
    assert_frame_equal(df_tr, df_output_transformer)


def test_add_features():

    my_pipeline = make_pipeline(InfraCleaner(), DomainCleaner(), AddFeatures())
    df_tr = my_pipeline.transform(df_input_start)
    assert_frame_equal(df_tr, df_output_addfeatures)


def test_feature_selector_numeric():

    my_pipeline = make_pipeline(
        InfraCleaner(), DomainCleaner(), AddFeatures(), FeatureSelector(np.number)
    )
    df_tr = my_pipeline.transform(df_input_start)
    assert_frame_equal(df_tr, df_output_select_numeric)


def test_feature_selector_category():

    my_pipeline = make_pipeline(
        InfraCleaner(), DomainCleaner(), AddFeatures(), FeatureSelector("category")
    )
    df_tr = my_pipeline.transform(df_input_start)
    assert_frame_equal(df_tr, df_output_select_category)


def test_regroup_categories_to_autre():

    my_pipeline = make_pipeline(
        InfraCleaner(),
        DomainCleaner(),
        AddFeatures(),
        FeatureSelector("category"),
        RegroupeCreateCategoryAutre(),
    )
    df_tr = my_pipeline.fit_transform(df_input_start)
    assert_frame_equal(df_tr, df_output_regroup_categories)


print(test_regroup_categories_to_autre())
