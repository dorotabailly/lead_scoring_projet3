"""
This module defines the transformers used in the model pipeline.
"""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

import src.settings.base as stg


class DomainCleaner(BaseEstimator, TransformerMixin):
    """Transformer class used to perform some cleanings"
    """

    def __init__(self):
        """ The fit methode"""
        pass

    def fit(self, X, y=None):
        """ The fit methode"""
        return self

    def transform(self, X, y=None):
        """The transform methode doing additional cleaning including the following steps :
        - outliers correction for the features "NB_VISITES" and "DUREE_SUR_SITEWEB_COL"
        - some categories groupings which are of common sense

        Parameters
        ----------
        X : pandas.core.frame.DataFrame
            input dataframe
        y : pandas.core.frame.DataFrame, optional
            target value, by default None

        Returns
        -------
        pandas.core.frame.DataFrame
            transformed dataframe
        """

        X = X.copy()
        return self._clean(X)

    def _clean(self, df):
        df = df.copy()
        df = self._correct_outliers_errors(df)
        df = self._correct_values(df)
        return df

    def _correct_outliers_errors(self, df):
        df = df.copy()
        mask_outlier = (df[stg.NB_VISITES_COL] != 0) & (df[stg.DUREE_SUR_SITEWEB_COL] == 0)
        df[stg.NB_VISITES_COL] = np.where(mask_outlier, np.nan, df[stg.NB_VISITES_COL])
        df[stg.DUREE_SUR_SITEWEB_COL] = np.where(
            mask_outlier, np.nan, df[stg.DUREE_SUR_SITEWEB_COL]
        )
        return df

    def _correct_values(self, df):
        df = df.copy()
        # Formulaire
        df[stg.ORIGINE_LEAD_COL] = df[stg.ORIGINE_LEAD_COL].replace(
            "formulaire quick add", "formulaire add"
        )
        df[stg.ORIGINE_LEAD_COL] = df[stg.ORIGINE_LEAD_COL].replace(
            "formulaire lead add", "formulaire add"
        )
        # Homme d'affaires
        df[stg.STATUT_ACTUEL_COL] = df[stg.STATUT_ACTUEL_COL].replace(
            "homme d'affaire", "en activite"
        )
        df[stg.STATUT_ACTUEL_COL] = df[stg.STATUT_ACTUEL_COL].replace(
            "professionnel en activite", "en activite"
        )
        # Dernière activité
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "reinscrit aux emails", "formulaire soumis sur le site"
        )
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "stand visite au salon", "approche directe"
        )
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "email marque comme spam", "ne veut pas de contact"
        )
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "desinscrit", "ne veut pas de contact"
        )
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "email rejete", "ne veut pas de contact"
        )
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "a clique sur le lien dans le navigateur", "a clique sur le lien"
        )
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "a clique sur le lien dans le mail", "a clique sur le lien"
        )
        df[stg.DERNIERE_ACTIVITE_COL] = df[stg.DERNIERE_ACTIVITE_COL].replace(
            "a clique sur le lien dand le navigateur", "a clique sur le lien"
        )
        return df


class AddFeatures(BaseEstimator, TransformerMixin):
    """ Transformer class used to add new features """

    def __init__(self):
        """ the fit methode"""
        return

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """the transform method adding new features. In the final model only one feature are created "NB_DUREE_MOY_PAR_VISITE"

        Parameters
        ----------
        X : pandas.core.frame.DataFrame
            input dataframe
        y : pandas.core.frame.DataFrame, optional
            target value, by default None

        Returns
        -------
        pandas.core.frame.DataFrame
            transformed dataframe
        """
        return self._add_features(X)

    def _add_features(self, df):
        df = df.copy()
        df = self._add_duree_moy_par_visite(df)
        return df

    @staticmethod
    def _add_duree_moy_par_visite(X):
        X = X.copy()
        X["NB_DUREE_MOY_PAR_VISITE"] = X["NB_VISITES"]
        X.loc[X["NB_VISITES"] > 0, ["NB_DUREE_MOY_PAR_VISITE"]] = (
            X["DUREE_SUR_SITEWEB"] / X["NB_VISITES"]
        )
        X.loc[X["NB_VISITES"] == 0, ["NB_DUREE_MOY_PAR_VISITE"]] = 0
        X = X.drop(["DUREE_SUR_SITEWEB"], axis=1)
        return X


class FeatureSelector(BaseEstimator, TransformerMixin):
    """Transformer used to select a subset of features(numerical vs. categorical)"""

    def __init__(self, _dtype):
        self._dtype = _dtype

    def fit(self, X, y=None):
        """ the fit methode"""
        return self

    def transform(self, X, y=None):
        """transform methode used to select a given type of features

        Parameters
        ----------
        X : pandas.core.frame.DataFrame
            input dataframe
        y : pandas.core.frame.DataFrame, optional
            target value, by default None

        Returns
        -------
        pandas.core.frame.DataFrame
            transformed dataframe
        """
        return X.select_dtypes(include=self._dtype)


class RegroupeCreateCategoryAutre(BaseEstimator, TransformerMixin):
    """Transformer class used to regroup categories with less than category_min_threshold
    and create the category "Autre" """

    def __init__(self):
        self.mapping = []
        pass

    def fit(self, X, y=None):
        """ The fit methode defines the categories to be grouped to the category "Autre" """
        categorial_col = X.select_dtypes(include="category").columns
        print(categorial_col)

        for col in categorial_col:

            counts = X[col].value_counts(dropna=False)
            mapping_list = list(counts[counts > stg.CATEGORY_MIN_THRESHOLD].index.dropna())
            self.mapping.append(mapping_list)

        return self

    def transform(self, X, y=None):
        """The transform methode groups the categories as defined by the fit methode to one category "Autre"

        Parameters
        ----------
        X : pandas.core.frame.DataFrame
            input dataframe
        y : pandas.core.frame.DataFrame, optional
            target value, by default None

        Returns
        -------
        pandas.core.frame.DataFrame
            transformed dataframe
        """

        X = X.copy()
        categorial_col = X.select_dtypes(include="category").columns

        i = 0
        for col in categorial_col:

            temp = X[col].apply(lambda x: x if x in self.mapping[i] else "autre")
            X[col] = temp
            i = i + 1

        return X
