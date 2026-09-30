from typing import Dict


def weighted_prompt_score(analysis: Dict) -> int:
    weights = {
        "clarity": 0.30,
        "specificity": 0.25,
        "context": 0.25,
        "constraints": 0.20,
    }
    score = sum(float(analysis.get(k, 0)) * w for k, w in weights.items())
    return max(0, min(100, round(score)))


def response_score(metrics: Dict[str, float]) -> float:
    values = [metrics.get(k, 0) for k in ("relevance", "clarity", "completeness", "specificity")]
    return round(sum(values) / 40 * 100, 1)
