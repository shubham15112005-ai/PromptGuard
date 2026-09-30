"""
PromptGuard - Prompt Strategy Recommender

Maps prompt weaknesses and task characteristics to appropriate
prompt-engineering strategies.

The recommender is deterministic so that its decisions are
repeatable and explainable during testing.
"""

from typing import Dict, List


STRATEGY_INFO = {
    "role prompting": {
        "description": "Assign a relevant expert role or perspective to the model.",
        "benefit": "Provides a clearer perspective, expertise level, and response style.",
    },
    "context injection": {
        "description": "Provide relevant background information, source material, or constraints.",
        "benefit": "Reduces ambiguity and gives the model information needed for a grounded response.",
    },
    "structured output": {
        "description": "Explicitly define the desired response structure or format.",
        "benefit": "Makes the response more predictable, readable, and easier to evaluate.",
    },
    "constraint prompting": {
        "description": "Specify boundaries such as length, scope, exclusions, or required conditions.",
        "benefit": "Controls the model's output and reduces unnecessary information.",
    },
    "few-shot prompting": {
        "description": "Provide one or more examples showing the expected input-output pattern.",
        "benefit": "Helps the model understand the desired task and output pattern.",
    },
    "zero-shot prompting": {
        "description": "Give a direct task instruction without providing examples.",
        "benefit": "Works well for straightforward tasks where the desired behavior is obvious.",
    },
    "decomposition": {
        "description": "Break a complex task into smaller, ordered subtasks.",
        "benefit": "Makes multi-step reasoning and complex tasks easier to manage.",
    },
}


def recommend_strategies(
    prompt: str,
    analysis: Dict,
) -> Dict:
    """
    Recommend prompt-engineering strategies based on analyzer output.

    Returns:
        {
            "primary_strategy": str,
            "recommended_strategies": [...],
            "explanations": [...],
            "strategy_details": [...]
        }
    """

    prompt = prompt.strip()
    lower = prompt.lower()

    recommended: List[str] = []
    explanations: List[str] = []

    quality = analysis.get("quality_score", 0)
    context = analysis.get("context", 0)
    constraints = analysis.get("constraints", 0)
    specificity = analysis.get("specificity", 0)
    ambiguity = analysis.get("ambiguity", "medium")

    missing = analysis.get("missing_information", [])
    issues = analysis.get("issues", [])

    # ---------------------------------------------------------
    # 1. ROLE PROMPTING
    # ---------------------------------------------------------

    if (
        context < 70
        or "target audience" in " ".join(missing).lower()
        or "role" in lower
    ):
        recommended.append("role prompting")
        explanations.append(
            "A clear role can establish the expertise, perspective, "
            "and communication style expected from the model."
        )

    # ---------------------------------------------------------
    # 2. CONTEXT INJECTION
    # ---------------------------------------------------------

    if (
        context < 65
        or any(
            word in " ".join(missing).lower()
            for word in ["context", "background"]
        )
    ):
        recommended.append("context injection")
        explanations.append(
            "Additional context can reduce ambiguity and give the model "
            "the information required to produce a grounded answer."
        )

    # ---------------------------------------------------------
    # 3. STRUCTURED OUTPUT
    # ---------------------------------------------------------

    if (
        constraints < 65
        or any(
            word in " ".join(missing).lower()
            for word in ["format", "output"]
        )
    ):
        recommended.append("structured output")
        explanations.append(
            "An explicit output structure makes the response more "
            "consistent and easier to read and evaluate."
        )

    # ---------------------------------------------------------
    # 4. CONSTRAINT PROMPTING
    # ---------------------------------------------------------

    if constraints < 70:
        recommended.append("constraint prompting")
        explanations.append(
            "Explicit constraints can control response length, scope, "
            "required elements, and unwanted content."
        )

    # ---------------------------------------------------------
    # 5. DECOMPOSITION
    # ---------------------------------------------------------

    complex_indicators = [
        "compare",
        "analyze",
        "design",
        "develop",
        "research",
        "plan",
        "build",
        "evaluate",
        "multiple",
        "and then",
        "step by step",
    ]

    complex_count = sum(
        indicator in lower for indicator in complex_indicators
    )

    if complex_count >= 2:
        recommended.append("decomposition")
        explanations.append(
            "The task contains multiple components, so breaking it into "
            "smaller steps can improve organization and reliability."
        )

    # ---------------------------------------------------------
    # 6. FEW-SHOT PROMPTING
    # ---------------------------------------------------------

    task_words = [
        "classify",
        "extract",
        "format",
        "rewrite",
        "convert",
        "categorize",
        "label",
        "generate",
    ]

    if (
        any(word in lower for word in task_words)
        and "example" not in lower
    ):
        recommended.append("few-shot prompting")
        explanations.append(
            "Examples can demonstrate the exact behavior or output pattern "
            "expected from the model."
        )

    # ---------------------------------------------------------
    # 7. ZERO-SHOT PROMPTING
    # ---------------------------------------------------------

    # Straightforward prompts do not always need examples.
    if (
        quality >= 70
        and specificity >= 65
        and not any(
            strategy in recommended
            for strategy in ["few-shot prompting", "decomposition"]
        )
    ):
        recommended.append("zero-shot prompting")
        explanations.append(
            "The prompt is already sufficiently clear for a direct "
            "instruction without examples."
        )

    # ---------------------------------------------------------
    # FALLBACK
    # ---------------------------------------------------------

    if not recommended:
        recommended = [
            "role prompting",
            "structured output",
            "constraint prompting",
        ]

        explanations = [
            "These techniques provide a general improvement baseline "
            "for an under-specified prompt."
        ]

    # Remove duplicates while preserving order.
    unique_recommended = list(dict.fromkeys(recommended))

    # ---------------------------------------------------------
    # PRIORITIZATION
    # ---------------------------------------------------------

    priority_order = [
        "context injection",
        "role prompting",
        "structured output",
        "constraint prompting",
        "decomposition",
        "few-shot prompting",
        "zero-shot prompting",
    ]

    ranked = sorted(
        unique_recommended,
        key=lambda x: priority_order.index(x)
        if x in priority_order
        else 999,
    )

    primary_strategy = ranked[0]

    # ---------------------------------------------------------
    # STRATEGY DETAILS
    # ---------------------------------------------------------

    strategy_details = []

    for strategy in ranked:
        info = STRATEGY_INFO[strategy]

        strategy_details.append(
            {
                "strategy": strategy,
                "description": info["description"],
                "benefit": info["benefit"],
            }
        )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    summary = (
        f"Prompt quality is {quality}/100 with {ambiguity} ambiguity. "
        f"The system recommends {len(ranked)} prompting strategies, "
        f"with '{primary_strategy}' as the primary recommendation."
    )

    return {
        "primary_strategy": primary_strategy,
        "recommended_strategies": ranked,
        "explanations": explanations,
        "strategy_details": strategy_details,
        "summary": summary,
    }