import json
import uuid
from typing import Dict, List, Tuple

import datasketch
import spacy
import treesimi


class MinHashScorer:
    def __init__(self) -> None:
        self.pipeline = spacy.load("de_dep_hdt_dist", disable=[
            'morphologizer', 'attribute_ruler', 'ner', 'lemmatizer'])
        self._treesimi_config = {
            "use_trunc_leaves": True,
            "use_drop_nodes": False,
            "use_replace_attr": False,
        }

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        ids = list(query_sents.keys())
        minhash_table = []
        for sent_id, sent_txt in query_sents.items():
            shingled_subtrees = self._text_to_shingles(sent_txt)
            minhash_table.append(self._minhash(shingled_subtrees))

        similarity_matrix = [
            [
                minhash_table[i].jaccard(minhash_table[j])
                for j in range(len(minhash_table))
            ]
            for i in range(len(minhash_table))
        ]
        return {"ids": ids, "matrix": similarity_matrix}

    def _text_to_shingles(self, text: str):
        # spacy might identify multiple subtrees with the same label.
        # thus, loop over all sentences identified by spacy
        shingled_all = []
        for adjac in treesimi.to_adjac_from_spacy(text, model=self.pipeline):
            # convert adjacency list to nested set model
            nested = treesimi.adjac_to_nested_with_attr(adjac)
            nested = treesimi.remove_node_ids(nested)
            # extract subtrees
            shingled = treesimi.shingleset(nested, **self._treesimi_config)
            shingled_all.extend(shingled)
        # cheesy trick: convert subtrees in `shingled` to strings.
        stringified = [json.dumps(tree).encode('utf-8')
                       for tree in shingled_all]
        return stringified

    def _minhash(self, shingled_subtrees: List[bytes]) -> datasketch.MinHash:
        minhash = datasketch.MinHash(num_perm=256)
        for s in shingled_subtrees:
            minhash.update(s)
        return minhash
