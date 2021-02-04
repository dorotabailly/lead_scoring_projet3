"This module creates an instance of the API used to predict the lead score."

import datetime
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domain.lead import Lead
from src.infrastructure.config.config import config


lead = Lead()
app = FastAPI(
    title="Lead scoring Yotta",
    description="This API calls a lead scoring model deployed on GKE. ",
    version="1.0.0",
)

PORT = config["api"]["port"]
HOST = config["api"]["host"]

app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_methods=["POST", "GET"], allow_headers=["*"]
)


@app.post("/")
def get_prediction(leads: List[dict]):

    """Main methode used to return the lead score with the API

    Parameters
    ----------
    leads : List[dict]
        features describing the lead

    Returns
    -------
    dict
        the score is given by the value of the doctionary
    """

    predictions = []

    for l in leads:
        prediction = lead.predict(l)
        predictions.append(prediction)

    return predictions


if __name__ == "__main__":
    print("starting API", datetime.datetime.now())
    uvicorn.run(app, host=HOST, port=PORT)
