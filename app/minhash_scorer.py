import json
import uuid
from typing import Dict, List, Tuple

import datasketch
import trankit
import treesimi


class MinHashScorer:
    def __init__(self) -> None:
        self.pipeline = trankit.Pipeline(
            lang="german", gpu=False, cache_dir="./cache"
        )
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
        for sent_id, sent in query_sents.items():
            processed = self._parse_dependencies(sent)
            adjac = self._convert_to_adjacency_list(processed)
            shingled_subtrees = self._convert_to_subtree_shingleset(adjac)
            minhash_table.append(self._minhash(shingled_subtrees))

        similarity_matrix = [
            [
                minhash_table[i].jaccard(minhash_table[j])
                for j in range(len(minhash_table))
            ]
            for i in range(len(minhash_table))
        ]
        return {"ids": ids, "matrix": similarity_matrix}

    def _parse_dependencies(self, sentence: str) -> dict:
        return self.pipeline.posdep(sentence, is_sent=True)

    def _convert_to_adjacency_list(
        self, parsed_sentence: dict
    ) -> list[Tuple[int, int, str]]:
        return [
            (token["id"], token["head"], token["deprel"])
            if isinstance(token["id"], int)
            else (
                token["expanded"][0]["id"],
                token["expanded"][0]["head"],
                token["expanded"][0]["deprel"],
            )
            for token in parsed_sentence["tokens"]
        ]

    def _convert_to_subtree_shingleset(
        self, adjacency_list: List[Tuple[int, int, str]]
    ) -> List[bytes]:
        nested = treesimi.adjac_to_nested_with_attr(adjacency_list)
        nested = treesimi.remove_node_ids(nested)
        shingled = treesimi.shingleset(nested, **self._treesimi_config)
        return [json.dumps(tree).encode("utf-8") for tree in shingled]

    def _minhash(self, shingled_subtrees: List[bytes]) -> datasketch.MinHash:
        minhash = datasketch.MinHash(num_perm=256)
        for s in shingled_subtrees:
            minhash.update(s)
        return minhash
