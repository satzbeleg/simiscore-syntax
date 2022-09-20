[![Join the chat at https://gitter.im/satzbeleg/community](https://badges.gitter.im/satzbeleg/community.svg)](https://gitter.im/satzbeleg/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/satzbeleg/simiscore-syntax.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/simiscore-syntax/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/satzbeleg/simiscore-syntax.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/simiscore-syntax/context:python)


# simiscore-syntax
An ML API to compute the Jaccard similarity based on shingled subtrees of the dependency grammar.
The API is programmed with the [`fastapi` Python package](https://fastapi.tiangolo.com/). 
Dependency trees are extracted with a [`spacy`](https://github.com/explosion/spaCy) model [trained on HDT](https://huggingface.co/reneknaebel/de_dep_hdt_dist).
The similarity scores are computed with the packages [`datasketch`](http://ekzhu.com/datasketch/index.html) and [`treesimi`](https://github.com/ulf1/treesimi).
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

## Citation

### References
- Sebastián Ramírez, 2018, FastAPI, [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)
- Ines Montani, Matthew Honnibal, Matthew Honnibal, Sofie Van Landeghem, Adriane Boyd, Henning Peters, Paul O'Leary McCann, Maxim Samsonov, Jim Geovedi, Jim O'Regan, Duygu Altinok, György Orosz, Søren Lind Kristiansen, Daniël de Kok, Lj Miranda, Roman, Explosion Bot, Leander Fiedler, Grégory Howard, … Björn Böing. (2022). explosion/spaCy: New Span Ruler component, JSON (de)serialization of Doc, span analyzer and more (v3.3.1). Zenodo. [https://doi.org/10.5281/zenodo.6621076](https://doi.org/10.5281/zenodo.6621076)
- Rene Knaebel. (2022). reneknaebel/de_dep_hdt_dist (v0.1.0). Huggingface. [https://huggingface.co/reneknaebel/de_dep_hdt_dist](https://huggingface.co/reneknaebel/de_dep_hdt_dist)
- Eric Zhu, Vadim Markovtsev, aastafiev, Wojciech Łukasiewicz, ae-foster, Sinusoidal36, Ekevoo, Kevin Mann, Keyur Joshi, Peter Kubov, Qin TianHuan, Spandan Thakur, Stefano Ortolani, Titusz, Vojtech Letal, Zac Bentley, fpug, & oisincar. (2021). ekzhu/datasketch: v1.5.4 (v1.5.4). Zenodo. [https://doi.org/10.5281/zenodo.5758425](https://doi.org/10.5281/zenodo.5758425)
- Ulf Hamster, & Luise Köhler. (2022). treesimi: Shingling for measuring tree similarity (0.1.6). Zenodo. [https://doi.org/10.5281/zenodo.6501989](https://doi.org/10.5281/zenodo.6501989)


### Support
Please [open an issue](https://github.com/satzbeleg/simiscore-syntax/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/simiscore-syntax/compare/).
