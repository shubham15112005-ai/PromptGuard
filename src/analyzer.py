"""
PromptGuard - Prompt Analyzer

Analyzes a user prompt using deterministic, explainable heuristics.
This provides a reproducible baseline before optional LLM-based analysis.
"""

import re
from typing import Dict, List


# Common signals used by the analyzer.
VAGUE_TERMS = {
    "something",
    "anything",
    "good",
    "better",
    "best",
    "nice",
    "stuff",
    "things",
    "tell me",
    "help me",
    "make it",
    "do it",
    "explain it",
    "fix this",
    "improve this",
}

ROLE_SIGNALS = {
    "act as",
    "you are",
    "role",
    "expert",
    "professor",
    "developer",
    "analyst",
    "teacher",
    "consultant",
}

AUDIENCE_SIGNALS = {
    "beginner",
    "student",
    "expert",
    "developer",
    "manager",
    "customer",
    "user",
    "child",
    "professional",
    "researcher",
    "audience",
}

FORMAT_SIGNALS = {
    "bullet",
    "bullets",
    "table",
    "steps",
    "step-by-step",
    "headings",
    "json",
    "xml",
    "markdown",
    "list",
    "paragraph",
    "format",
}

CONSTRAINT_SIGNALS = {
    "under",
    "less than",
    "maximum",
    "minimum",
    "limit",
    "only",
    "must",
    "should",
    "avoid",
    "do not",
    "don't",
    "exactly",
    "within",
    "between",
}

CONTEXT_SIGNALS = {
    "because",
    "for",
    "using",
    "based on",
    "context",
    "background",
    "given",
    "following",
    "project",
    "course",
    "company",
    "dataset",
    "document",
}

OUTPUT_SIGNALS = {
    "explain",
    "summarize",
    "compare",
    "generate",
    "create",
    "write",
    "analyze",
    "calculate",
    "design",
    "list",
    "recommend",
    "convert",
}


def _contains_signal(text: str, signals: set) -> bool:
    """Return True when at least one signal occurs in the text."""
    text = text.lower()
    return any(signal in text for signal in signals)


def _find_matches(text: str, signals: set) -> List[str]:
    """Return the signals found in the prompt."""
    text = text.lower()
    return [signal for signal in signals if signal in text]


def _word_count(prompt: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", prompt))


def _sentence_count(prompt: str) -> int:
    sentences = re.split(r"[.!?]+", prompt.strip())
    return len([s for s in sentences if s.strip()])


def analyze_prompt(prompt: str) -> Dict:
    """
    Analyze a prompt and return structured quality information.

    Scores are deliberately deterministic so experiments can be repeated
    with the same input.
    """

    prompt = prompt.strip()

    if not prompt:
        return {
            "quality_score": 0,
            "clarity": 0,
            "specificity": 0,
            "context": 0,
            "constraints": 0,
            "ambiguity": "high",
            "hallucination_risk": "high",
            "missing_information": [
                "A task or question",
                "Context",
                "Expected output",
            ],
            "issues": ["The prompt is empty."],
            "recommended_techniques": [
                "role prompting",
                "structured output",
                "constraint prompting",
            ],
            "reasoning_summary": "No prompt was provided for analysis.",
        }

    lower = prompt.lower()
    words = _word_count(prompt)
    sentences = _sentence_count(prompt)

    vague_matches = _find_matches(prompt, VAGUE_TERMS)

    has_role = _contains_signal(prompt, ROLE_SIGNALS)
    has_audience = _contains_signal(prompt, AUDIENCE_SIGNALS)
    has_format = _contains_signal(prompt, FORMAT_SIGNALS)
    has_constraints = _contains_signal(prompt, CONSTRAINT_SIGNALS)
    has_context = _contains_signal(prompt, CONTEXT_SIGNALS)
    has_output_instruction = _contains_signal(prompt, OUTPUT_SIGNALS)

    # ---------------------------------------------------------
    # 1. CLARITY
    # ---------------------------------------------------------

    clarity = 45

    if words >= 6:
        clarity += 10

    if words >= 12:
        clarity += 10

    if words >= 20:
        clarity += 5

    if has_output_instruction:
        clarity += 10

    if sentences >= 2:
        clarity += 5

    if vague_matches:
        clarity -= min(25, len(vague_matches) * 8)

    clarity = max(0, min(100, clarity))

    # ---------------------------------------------------------
    # 2. SPECIFICITY
    # ---------------------------------------------------------

    specificity = 35

    if words >= 10:
        specificity += 10

    if words >= 20:
        specificity += 10

    if words >= 35:
        specificity += 10

    if has_output_instruction:
        specificity += 10

    if has_format:
        specificity += 10

    if has_constraints:
        specificity += 10

    specificity = max(0, min(100, specificity))

    # ---------------------------------------------------------
    # 3. CONTEXT
    # ---------------------------------------------------------

    context = 25

    if has_context:
        context += 25

    if has_audience:
        context += 20

    if has_role:
        context += 10

    if words >= 20:
        context += 10

    context = max(0, min(100, context))

    # ---------------------------------------------------------
    # 4. CONSTRAINTS
    # ---------------------------------------------------------

    constraints = 20

    if has_format:
        constraints += 25

    if has_constraints:
        constraints += 30

    if has_audience:
        constraints += 10

    if "length" in lower or "words" in lower:
        constraints += 10

    constraints = max(0, min(100, constraints))

    # ---------------------------------------------------------
    # ISSUES
    # ---------------------------------------------------------

    issues = []
    missing_information = []

    if words < 6:
        issues.append("The prompt is very short and may not contain enough task context.")

    if vague_matches:
        issues.append(
            "The prompt contains vague or ambiguous wording: "
            + ", ".join(vague_matches[:4])
        )

    if not has_audience:
        missing_information.append("Target audience or expertise level")

    if not has_context:
        missing_information.append("Relevant background or task context")

    if not has_format:
        missing_information.append("Preferred output format")

    if not has_constraints:
        missing_information.append("Specific constraints or requirements")

    if not has_output_instruction:
        issues.append("The desired task or output is not clearly specified.")

    if not issues:
        issues.append("No major structural issues detected.")

    # ---------------------------------------------------------
    # AMBIGUITY
    # ---------------------------------------------------------

    ambiguity_points = 0

    if words < 6:
        ambiguity_points += 3

    if vague_matches:
        ambiguity_points += min(3, len(vague_matches))

    if not has_output_instruction:
        ambiguity_points += 2

    if not has_context:
        ambiguity_points += 1

    if ambiguity_points >= 5:
        ambiguity = "high"
    elif ambiguity_points >= 3:
        ambiguity = "medium"
    else:
        ambiguity = "low"

    # ---------------------------------------------------------
    # HALLUCINATION RISK
    # ---------------------------------------------------------

    risk_points = 0

    if not has_context:
        risk_points += 2

    if not has_constraints:
        risk_points += 1

    if words < 8:
        risk_points += 2

    # High-risk domains/requests need stronger grounding.
    factual_terms = {
        "latest",
        "current",
        "today",
        "statistics",
        "price",
        "medical",
        "legal",
        "financial",
        "research",
        "citation",
        "source",
    }

    if any(term in lower for term in factual_terms):
        risk_points += 2

    if risk_points >= 5:
        hallucination_risk = "high"
    elif risk_points >= 3:
        hallucination_risk = "medium"
    else:
        hallucination_risk = "low"

    # ---------------------------------------------------------
    # RECOMMENDED PROMPTING TECHNIQUES
    # ---------------------------------------------------------

    techniques = []

    if not has_role:
        techniques.append("role prompting")

    if not has_context:
        techniques.append("context injection")

    if not has_format:
        techniques.append("structured output")

    if not has_constraints:
        techniques.append("constraint prompting")

    if words < 15:
        techniques.append("zero-shot refinement")

    if has_complex_task(prompt):
        techniques.append("decomposition")

    if "example" not in lower and words >= 15:
        techniques.append("few-shot prompting")

    # Remove duplicates while preserving order.
    techniques = list(dict.fromkeys(techniques))

    # ---------------------------------------------------------
    # FINAL SCORE
    # ---------------------------------------------------------

    quality_score = round(
        clarity * 0.30
        + specificity * 0.25
        + context * 0.25
        + constraints * 0.20
    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    summary = (
        f"The prompt received an overall quality score of {quality_score}/100. "
        f"Clarity is {clarity}/100, specificity is {specificity}/100, "
        f"context is {context}/100, and constraint coverage is "
        f"{constraints}/100. "
        f"Ambiguity is {ambiguity} and estimated hallucination risk is "
        f"{hallucination_risk}."
    )

    return {
        "quality_score": quality_score,
        "clarity": clarity,
        "specificity": specificity,
        "context": context,
        "constraints": constraints,
        "ambiguity": ambiguity,
        "hallucination_risk": hallucination_risk,
        "missing_information": missing_information,
        "issues": issues,
        "recommended_techniques": techniques,
        "reasoning_summary": summary,
    }


def has_complex_task(prompt: str) -> bool:
    """
    Detect tasks that may benefit from decomposition.
    """
    lower = prompt.lower()

    complex_signals = [
        "compare",
        "design",
        "develop",
        "build",
        "analyze",
        "research",
        "plan",
        "step by step",
        "multiple",
        "and then",
        "first",
        "second",
        "finally",
    ]

    return sum(signal in lower for signal in complex_signals) >= 2