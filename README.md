# Lead Scoring Yotta project
# Dorota Bailly et Jérôme Blin

[![pipeline status](https://gitlab.com/yotta-academy/mle-bootcamp/projects/ml-prod-projects/fall-2020/chaos-3/badges/develop/pipeline.svg)](https://gitlab.com/yotta-academy/mle-bootcamp/projects/ml-prod-projects/fall-2020/chaos-3/-/commits/develop)
[![coverage report](https://gitlab.com/yotta-academy/mle-bootcamp/projects/ml-prod-projects/fall-2020/chaos-3/badges/develop/coverage.svg)](https://gitlab.com/yotta-academy/mle-bootcamp/projects/ml-prod-projects/fall-2020/chaos-3/-/commits/develop)


The project in this repository creates and deploys an API on Google Kubernetes Engine (GKE), to expose a model for lead scoring. 

Additionally, a webapp was created alongisde this API to provide a graphical user interface to interact with it. The source code for this webapp is available on [this Github](https://github.com/blinjrm/yotta_leads), and the app is deployed on Streamlit Share. 

You can access the webapp [here](https://share.streamlit.io/blinjrm/yotta_leads/main/webapp.py)

The webapp is the privileged way to interact with the API, however if you want more control you can follow these steps to clone and use the code on your machine:

## 1. Clone this repository:

- Using SSH:
```
git@gitlab.com:yotta-academy/mle-bootcamp/projects/ml-prod-projects/fall-2020/chaos-3.git
```
- Using HTTPS:
```
https://gitlab.com/yotta-academy/mle-bootcamp/projects/ml-prod-projects/fall-2020/chaos-3.git
```

## 2. Setup

Make sure you have python >= 3.8 installed, and then install poetry using:
```
pip3 install poetry
```
Then change directory and install the project in a virtual environment:
```
cd chaos-3
poetry install
```

## 3. Activate the API

Run the following command to locally start the terminal:
```
uvicorn src.application.server:app
```

## 4. Use the API

In another terminal, run:
```
ipython3
```

This will open an ipython console, where you can directly type python code:
```
import requests

URL = "http://127.0.0.1:8000"
input = [
    {
        "ID_CLIENT": 628707,
        "ORIGINE_LEAD": "Formulaire Lead Add",
        "SOURCE_LEAD": "Olark Chat",
        "CONTACT_PAR_MAIL": "Non",
        "STATUT_ACTUEL": "Sans emploi",
        "NB_VISITES": 0,
        "DUREE_SUR_SITEWEB": 0,
        "DERNIERE_ACTIVITE": "Email ouvert",
        "VILLE": "Select",
        "SPECIALISATION": "Marketing Management",
        "Comment avez-vous entendu parler de nous ?": "Select",
        "Souhaites-tu recevoir une copie de notre livre blanc ?": "Non",
    }
]

pred = requests.post(URL, json=input)
print(pred, pred.text)
```

You should see the response and prediction from the API printed in the terminal:
```
<Response [200]> [{"result":0.6844176750798613}]
```
