from .recommender import recommend_strategies
from .analyzer import analyze_prompt
from .demo import answer_demo, evaluate_demo, optimize_demo
from .llm import chat, chat_json, is_live_mode
from .prompts import (
    ANALYSIS_SYSTEM,
    ANALYSIS_USER,
    ANSWER_SYSTEM,
    EVALUATE_SYSTEM,
    EVALUATE_USER,
    OPTIMIZE_SYSTEM,
    OPTIMIZE_USER,
)


def analyze(prompt: str, demo: bool = False):
    """
    Analyze a prompt.

    Demo mode:
        Uses the deterministic PromptGuard analyzer.

    Live mode:
        Uses the LLM analyzer while retaining a deterministic fallback
        if the LLM response cannot be parsed.
    """

    baseline = analyze_prompt(prompt)

    if demo or not is_live_mode():
        return baseline

    try:
        data = chat_json(
            ANALYSIS_SYSTEM,
            ANALYSIS_USER.format(prompt=prompt),
        )

        # Keep the deterministic score as a baseline reference.
        data["baseline_quality_score"] = baseline["quality_score"]

        return data

    except Exception:
        # The application should still work if the LLM analyzer fails.
        baseline["reasoning_summary"] += (
            " Live LLM analysis was unavailable, so the deterministic "
            "baseline analyzer was used."
        )
        return baseline

def recommend(prompt: str, analysis: dict, demo: bool = False):
    """
    Recommend appropriate prompt-engineering strategies.
    """
    return recommend_strategies(prompt, analysis)

def optimize(prompt: str, analysis: dict, demo: bool = False):
    """Generate an optimized version of the user's prompt."""

    if demo or not is_live_mode():
        return optimize_demo(prompt, analysis)

    return chat_json(
        OPTIMIZE_SYSTEM,
        OPTIMIZE_USER.format(
            prompt=prompt,
            analysis=analysis,
        ),
    )


def generate(prompt: str, demo: bool = False):
    """Generate a response to a prompt."""

    if demo or not is_live_mode():
        return answer_demo(prompt)

    return chat(
        ANSWER_SYSTEM,
        prompt,
        temperature=0.4,
    )


def evaluate(
    prompt: str,
    original: str,
    optimized: str,
    demo: bool = False,
):
    """Evaluate original and optimized responses."""

    if demo or not is_live_mode():
        return evaluate_demo(original, optimized)

    return chat_json(
        EVALUATE_SYSTEM,
        EVALUATE_USER.format(
            prompt=prompt,
            original=original,
            optimized=optimized,
        ),
    )
