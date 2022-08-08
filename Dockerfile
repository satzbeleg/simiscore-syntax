FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# see https://huggingface.co/spacy/de_dep_news_trf
# RUN python -m spacy download de_dep_news_trf

COPY ./app /app/app
