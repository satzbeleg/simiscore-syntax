from fastapi import FastAPI
from typing import Dict, List, Union
import uuid

from app.minhash_scorer import MinHashScorer


srvurl = ""

# basic information
app = FastAPI(
    title="Simiscore-Syntax ML API",
    descriptions=(
        "ML API to return the jaccard similarity score based serialized and"
        " shingled dependency grammar subtrees"
    ),
    version="0.1.0",
    openapi_url=f"{srvurl}/openapi.json",
    docs_url=f"{srvurl}/docs",
    redoc_url=f"{srvurl}/redoc",
)

similarity_scorer = MinHashScorer()


@app.get(f"{srvurl}/")
def get_info() -> dict:
    """Returns basic information about the application"""
    return {"version": app.version}


@app.post(f"{srvurl}/similarities/", response_model=Dict[str, list])
async def compute_similarites(
    query_sents: Union[List[str], Dict[uuid.UUID, str]],
) -> Dict[str, list]:
    if isinstance(query_sents, list):
        query_sents = {uuid.uuid4(): sentence for sentence in query_sents}
    return similarity_scorer.compute_similarity_matrix(query_sents)
