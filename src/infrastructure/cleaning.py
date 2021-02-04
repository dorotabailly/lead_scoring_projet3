""" 
Technical cleaning
"""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

import src.settings.base as stg


class InfraCleaner(BaseEstimator, TransformerMixin):
    """Transformer doing the technical cleaning for a dataframe describing lead features"""

    def __init__(self):
        """ The fit methode """
        pass

    def fit(self, X, y=None):
        """ The fit methode """
        return self

    def transform(self, X, y=None):
        """The transform methode doing the technical cleaning of data describing leads. The transformer includes following steps :
        - features selection used for the prediction
        - french accent remove
        - conversion to lower case
        - convert categorial features to type category

        Parameters
        ----------
        X : pandas DataFrame
            dataframe contaning features describing leads
        y : pandas.core.frame.DataFrame, optional
            target value, by default None


        Returns
        -------
        pandas DataFrame
        """

        X = X.copy()
        return self._clean_dataset(X)

    def _clean_dataset(self, df):

        df = df.copy()
        df = self._select_features(df)
        df = self._remove_accents(df)
        df = self._remove_upper_case(df)

        if stg.ID_CLIENT_COL in df.columns:
            df = df.set_index(stg.ID_CLIENT_COL)
        else:
            df = df
        df = self._change_object_type_to_category(df)
        return df

    @staticmethod
    def _select_features(df):
        df = df.copy()
        columns_to_extract = []
        for col in stg.FEATURES_TO_KEEP:
            if col in df.columns:
                columns_to_extract.append(col)
        df = df[columns_to_extract]
        return df

    @staticmethod
    def _remove_accents(df):
        df = df.copy()
        cols = df.select_dtypes(include=[np.object]).columns.to_list()
        df[cols] = df[cols].apply(
            lambda x: x.str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )
        return df

    @staticmethod
    def _remove_upper_case(df):
        df = df.copy()
        cols = df.select_dtypes(include=[np.object]).columns.to_list()
        df[cols] = df[cols].apply(lambda x: x.str.lower())
        return df

    @staticmethod
    def _change_object_type_to_category(df):
        df = df.copy()
        categorial_cols = df.select_dtypes(include=object).columns
        for col in categorial_cols:
            df[col] = df[col].astype("category")
        return df
