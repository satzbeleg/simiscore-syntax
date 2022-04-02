FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Download model into image (error 137 => allocate more RAM/HDD)
RUN python -c 'import trankit; trankit.Pipeline(lang="german", gpu=False, cache_dir="./cache")'

COPY ./app /app/app
