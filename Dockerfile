FROM python:3.8-slim

COPY . /chaos
WORKDIR /chaos

RUN apt-get update

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

RUN poetry install

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "src.application.server:app","--host" ,"0.0.0.0" , "--port" , "8000"]