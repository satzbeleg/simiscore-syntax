[![Join the chat at https://gitter.im/satzbeleg/community](https://badges.gitter.im/satzbeleg/community.svg)](https://gitter.im/satzbeleg/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


# simiscore-syntax
ML API to compute the Jaccard similarity score based on serialized and shingled dependency grammar subtrees.
The API is programmed with the [`fastapi` Python package](https://fastapi.tiangolo.com/), 
uses the packages [`datasketch`](http://ekzhu.com/datasketch/index.html), [`kshingle`](https://github.com/ulf1/kshingle), and [`treesimi`](https://github.com/ulf1/treesimi) to compute similarity scores.
The deployment is configured for Docker Compose.

## Docker Deployment
Call Docker Compose

```sh
export API_PORT=8084
docker-compose -f docker-compose.yml up --build

# or as oneliner:
API_PORT=8084 docker-compose -f docker-compose.yml up --build
```

(Start docker daemon before, e.g. `open /Applications/Docker.app` on MacOS).

Check

```sh
curl http://localhost:8084
```

Notes: Only `main.py` is used in `Dockerfile`.



## Local Development

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)


### Download spacy model
```sh
source .venv/bin/activate
```

### Start Server

```sh
source .venv/bin/activate
# uvicorn app.main:app --reload
gunicorn app.main:app --reload --bind=0.0.0.0:8084 \
    --worker-class=uvicorn.workers.UvicornH11Worker \
    --workers=1 --timeout=600
```

### Run some requests
The following example should yield a high similarity score because both sentences exhibit an identical syntactic structure:

```sh
curl -X POST "http://localhost:8084/similarities/" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '["Die Katze miaut.", "Der Hund bellte laut."]'
```

The example below should yield a lower similarity score because the two sentences differ in their syntactic structure:

```sh
curl -X POST "http://localhost:8084/similarities/" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '["Leise rieselt der Schnee.", "Der Schnee rieselt leise."]'
```

The example below should yield a low similarity score because the two sentences differ a lot with regard to their syntactic structure.

```sh
curl -X POST "http://localhost:8084/similarities/"  \
   -H "accept: application/json"  \
   -H "Content-Type: application/json"   \
   -d '["Der Schneemann ist groß.", "Die Kinder spielen im Schnee."]'
```

### Other commands and help
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`
- Show the docs: [http://localhost:8084/docs](http://localhost:8084/docs)
- Show Redoc: [http://localhost:8084/redoc](http://localhost:8084/redoc)


### Clean up 
```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


## Appendix

### Support
Please [open an issue](https://github.com/satzbeleg/simiscore-syntax/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/simiscore-syntax/compare/).
