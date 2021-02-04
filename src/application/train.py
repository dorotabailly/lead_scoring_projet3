"""This module defines the pipeline used for the model training and trains the model.""" 

import os
import pickle
from warnings import simplefilter

import category_encoders as ce
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline

import src.settings.base as stg
from src.domain.features_eng import (
    AddFeatures,
    DomainCleaner,
    FeatureSelector,
    RegroupeCreateCategoryAutre,
)
from src.infrastructure.cleaning import InfraCleaner

simplefilter(action="ignore", category=FutureWarning)


import category_encoders as ce
from sklearn.impute import SimpleImputer
from sklearn.metrics import precision_score
from sklearn.pipeline import Pipeline, make_pipeline, make_union


def create_data_pipeline():
    """ This methode defines the pipeline used for the model training. The applied transformations depend on the type of the feature.
    
    Returns
    -------
    sklearn.pipeline.Pipeline
        pipeline used for the model training
    """
    num_pipeline = make_pipeline(
        FeatureSelector(np.number),
        SimpleImputer(strategy="median", add_indicator=True),
    )

    cat_pipeline = make_pipeline(
        FeatureSelector("category"),
        RegroupeCreateCategoryAutre(),
        SimpleImputer(strategy="most_frequent", add_indicator=True),
        ce.TargetEncoder(),
    )

    data_pipeline = make_union(num_pipeline, cat_pipeline)

    return data_pipeline


def create_preprocessing_pipeline():
    """ This methode defines the pipeline used for the technical cleaning and for constructing new features

    Returns
    -------
    sklearn.pipeline.Pipeline
        pipeline used for the preprocessing 
    """    
    preprocessing_pipeline = make_pipeline(InfraCleaner(), DomainCleaner(), AddFeatures())

    return preprocessing_pipeline


def train(df):
    """This methode trains the model, includes a step for the hyperparameter optimisation and saves the trained model in a pickle file.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame containing the features used for the training
    """

    X = df.drop(columns=stg.TARGET)
    y = df[stg.TARGET].values

    preprocessing_pipeline = create_preprocessing_pipeline()
    data_pipeline = create_data_pipeline()
    model_pipeline = make_pipeline(data_pipeline, RandomForestClassifier(random_state=stg.SEED_RF))

    param_grid = {
        "randomforestclassifier__n_estimators": [30, 50, 70],
        "randomforestclassifier__min_samples_split": [5, 10],
        "randomforestclassifier__max_depth": [3, 5, 7, 9],
    }

    X_preprocessing = preprocessing_pipeline.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X_preprocessing, y, test_size=0.2, random_state=stg.SEED_TRAIN_TEST
    )

    gs = GridSearchCV(estimator=model_pipeline, param_grid=param_grid, cv=5)
    gs.fit(X_train, y_train)

    max_depth = gs.best_params_["randomforestclassifier__max_depth"]
    min_samples_split = min_samples_split = gs.best_params_[
        "randomforestclassifier__min_samples_split"
    ]
    nb_estimators = gs.best_params_["randomforestclassifier__n_estimators"]

    rf = RandomForestClassifier(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        n_estimators=nb_estimators,
        random_state=stg.SEED_RF,
    )
    model_pipeline = make_pipeline(data_pipeline, rf)

    model_pipeline.fit(X_train, y_train)
    y_pred = model_pipeline.predict(X_test)

    print(
        f"The model was successfully trained, with a precision of {precision_score(y_test, y_pred)}%."
    )

    MODEL_PATH = os.path.join(stg.MODEL_DIR, "model.pkl")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model_pipeline, f)


if __name__ == "__main__":
    df = pd.read_csv("".join((stg.TRAINING_DATA_DIR, "data_train.csv")), sep=";")
    train(df)
