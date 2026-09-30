from src.scorer import response_score, weighted_prompt_score


def test_weighted_prompt_score():
    analysis = {"clarity": 80, "specificity": 80, "context": 60, "constraints": 40}
    assert weighted_prompt_score(analysis) == 67


def test_response_score():
    metrics = {"relevance": 8, "clarity": 8, "completeness": 6, "specificity": 8}
    assert response_score(metrics) == 75.0
