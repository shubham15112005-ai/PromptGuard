from typing import Dict


def analyze_demo(prompt: str) -> Dict:
    words = prompt.split()
    vague_terms = ["something", "good", "best", "tell me", "help me", "it", "that"]
    found = [term for term in vague_terms if term in prompt.lower()]
    missing = []
    issues = []

    clarity = 78 if len(words) >= 8 else 55
    specificity = 72 if len(words) >= 12 else 48
    context = 45 if len(words) < 12 else 65
    constraints = 35

    if found:
        clarity -= min(25, len(found) * 7)
        issues.append("The prompt contains broad or ambiguous wording.")
    if not any(x in prompt.lower() for x in ["for", "audience", "student", "customer", "developer"]):
        missing.append("Target audience or use case")
    if not any(x in prompt.lower() for x in ["format", "bullet", "table", "steps", "headings"]):
        missing.append("Preferred output format")
    if len(words) < 8:
        missing.append("More task context and constraints")
        issues.append("The task is too short to reliably communicate all requirements.")
    else:
        issues.append("The task could still benefit from explicit output constraints.")

    risk = "high" if len(words) < 5 else ("medium" if len(missing) >= 2 else "low")
    techniques = ["role prompting", "structured output", "constraint prompting"]

    score = round(clarity * .30 + specificity * .25 + context * .25 + constraints * .20)
    return {
        "quality_score": score,
        "clarity": clarity,
        "specificity": specificity,
        "context": context,
        "constraints": constraints,
        "ambiguity": "high" if found else "medium",
        "hallucination_risk": risk,
        "missing_information": missing,
        "issues": issues,
        "recommended_techniques": techniques,
        "reasoning_summary": "Demo-mode heuristic analysis. Connect a Groq API key for LLM-based analysis."
    }


def optimize_demo(prompt: str, analysis: Dict) -> Dict:
    optimized = (
        "Act as an expert relevant to the task. "
        f"Complete the following request clearly and accurately: {prompt.strip()} "
        "Use clear headings and concise bullet points where useful. "
        "State important assumptions, avoid unsupported claims, and keep the response focused on the requested task."
    )
    return {
        "optimized_prompt": optimized,
        "changes": [
            "Added a suitable expert role.",
            "Added clarity and output-structure guidance.",
            "Added an instruction to avoid unsupported claims."
        ],
        "techniques_used": ["role prompting", "structured output", "constraint prompting"]
    }


def answer_demo(prompt: str) -> str:
    return (
        "Demo Mode response.\n\n"
        "This response is generated without an external LLM API. Add GROQ_API_KEY "
        "to enable live Generative AI responses and evaluation.\n\n"
        f"Task received: {prompt}"
    )


def evaluate_demo(original: str, optimized: str) -> Dict:
    return {
        "original": {"relevance": 6, "clarity": 6, "completeness": 5, "specificity": 5},
        "optimized": {"relevance": 8, "clarity": 8, "completeness": 7, "specificity": 8},
        "overall_original": 55,
        "overall_optimized": 78,
        "improvement_percent": 41.8,
        "winner_reason": "Demo-mode illustrative evaluation. Live mode evaluates actual LLM responses.",
        "limitations": ["Demo mode does not measure real model outputs."]
    }
