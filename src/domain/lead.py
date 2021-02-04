"""
Module to predict the score of a lead based on the trained model
"""

import os
import pickle

import pandas as pd

from src.application.train import create_preprocessing_pipeline


this_dir = os.path.dirname(os.path.realpath(__file__))


class Lead:
    """Class used to predict the score with the trained model

    Class attributes
    ----------------
    MODEL_PATH : str
        path to the model saved with pickle format


    Attributes
    ----------
    pipeline : scikitlearn pipeline
        pipeline used to predict the score

    """

    MODEL_PATH = os.path.join(this_dir, "model.pkl")

    def __init__(self):
        """ initialize the instance with a pickle model """
        with open(self.MODEL_PATH, "rb") as handle:
            self.pipeline = pickle.load(handle)

    def predict(self, lead_data: dict) -> dict:
        """methode used to predict the score for a lead

        Parameters
        ----------
        lead_data : dictionnary
            dictionnary with features describing the lead

        Returns
        -------
        dictionary
            dictionary containing the predicted score

        """

        lead_df = pd.DataFrame([lead_data])

        preprocessing_pipeline = create_preprocessing_pipeline()
        lead_df_preprocessing = preprocessing_pipeline.transform(lead_df)

        result = self.pipeline.predict_proba(lead_df_preprocessing)[0, 1]

        return {"result": result}
