import pytest
from app.minhash_scorer import MinHashScorer


@pytest.fixture(scope="module")
def scorer():
    return MinHashScorer()


@pytest.fixture
def sentences():
    return [
        "Einen Brief quer durch die USA schicken – in nur 10 Tagen!",
        "Eine revolutionäre Entwicklung, dauerte der Postversand um 1850 ein"
        "bis zwei Monate.",
        "Möglich machte es der sogenannte Pony-Express.",
        "Am 3. April 1860 begann eine Stafette furchtloser junger Männer, "
        "entlang der mehr als 3000 km langen Strecke zwischen Kalifornien und "
        "Missouri zuzustellen – hoch zu Ross, den widrigen Wetterverhältnissen"
        " und Überfällen trotzend.",
        "Allem Pioniergeist zum Trotz schienen die Gründer jedoch aufs Pferd "
        "gesetzt zu haben.",
        "Denn bereits 18 Monate später wurde der Pony-Express eingestellt.",
        "Zwei Tage, nachdem das erste transkontinentale Telegramm per "
        "verschickt wurde.",
    ]


def test_score_for_same_sentence(scorer, sentences):
    test_sentences = {"a": sentences[1], "b": sentences[1]}
    result = scorer.compute_similarity_matrix(test_sentences)["matrix"][0][1]
    assert pytest.approx(result) == 1.0


def test_score_for_different_sentences(scorer, sentences):
    test_sentences = {
        "a": sentences[0],
        "b": sentences[1],
    }
    result = scorer.compute_similarity_matrix(test_sentences)["matrix"][0][1]
    assert 0.5 - result >= 0


def test_id_extraction(scorer, sentences):
    test_sentences = {
        i: sent for i in range(len(sentences)) for sent in sentences
    }
    result = scorer.compute_similarity_matrix(test_sentences)["ids"]
    expected = [0, 1, 2, 3, 4, 5, 6]
    assert result == expected


def test_empty_query(scorer, sentences):
    query = {}
    result = scorer.compute_similarity_matrix(query)
    expected = {"ids": [], "matrix": []}
    assert result == expected


def test_query_only_one_sentence(scorer, sentences):
    query = {"a": sentences[2]}
    result = scorer.compute_similarity_matrix(query)["matrix"][0][0]
    assert pytest.approx(result) == 1


def test_multiple_sentences(scorer, sentences):
    test_sentences = sentences * 3
    query = {
        i: sent for i in range(len(test_sentences)) for sent in test_sentences
    }
    result = scorer.compute_similarity_matrix(query)["matrix"][0][
        len(sentences)
    ]
    assert pytest.approx(result) == 1
