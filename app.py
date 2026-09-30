import streamlit as st
from src.engine import analyze, recommend, optimize, generate, evaluate

st.set_page_config(
    page_title="PromptGuard | AI Prompt Quality",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: 800;
}
.subtitle {
    font-size: 20px;
    color: #666;
}
.score {
    font-size: 34px;
    font-weight: 700;
}
.card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🛡️ PromptGuard")
demo_mode = st.sidebar.toggle("Demo Mode", value=True)

st.sidebar.markdown("---")
st.sidebar.subheader("Pipeline")
st.sidebar.write("1. 🔍 Prompt Analyzer")
st.sidebar.write("2. 🧠 Strategy Recommender")
st.sidebar.write("3. ✨ Prompt Optimizer")
st.sidebar.write("4. 🤖 Response Generator")
st.sidebar.write("5. 📊 Evaluation Engine")

st.sidebar.markdown("---")
st.sidebar.caption("GenAI & Prompt Engineering Course Project")

st.markdown(
    '<div class="main-title">🛡️ PromptGuard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI Prompt Quality & Optimization System</div>',
    unsafe_allow_html=True
)

st.write(
    "Analyze a prompt → recommend techniques → optimize it → "
    "generate responses → evaluate improvement."
)

prompt = st.text_area(
    "Enter your prompt",
    height=180,
    placeholder="Example: Explain machine learning to a beginner..."
)

col1, col2 = st.columns(2)

with col1:
    analyze_button = st.button(
        "🔍 Analyze Prompt",
        use_container_width=True,
        type="primary"
    )

with col2:
    full_button = st.button(
        "🚀 Run Full Optimization",
        use_container_width=True
    )

if analyze_button and prompt.strip():

    analysis = analyze(prompt, demo=demo_mode)
    recommendation = recommend(prompt, analysis, demo=demo_mode)

    st.session_state["prompt"] = prompt
    st.session_state["analysis"] = analysis
    st.session_state["recommendation"] = recommendation

if full_button and prompt.strip():

    with st.spinner("Running PromptGuard pipeline..."):

        analysis = analyze(prompt, demo=demo_mode)
        recommendation = recommend(prompt, analysis, demo=demo_mode)
        optimized = optimize(prompt, analysis, demo=demo_mode)
        original_response = generate(prompt, demo=demo_mode)

        if isinstance(optimized, dict):
            optimized_prompt = optimized.get(
                "optimized_prompt",
                optimized.get("prompt", str(optimized))
            )
        else:
            optimized_prompt = str(optimized)

        optimized_response = generate(
            optimized_prompt,
            demo=demo_mode
        )

        evaluation = evaluate(
            prompt,
            original_response,
            optimized_response,
            demo=demo_mode
        )

        st.session_state["prompt"] = prompt
        st.session_state["analysis"] = analysis
        st.session_state["recommendation"] = recommendation
        st.session_state["optimized"] = optimized_prompt
        st.session_state["original_response"] = original_response
        st.session_state["optimized_response"] = optimized_response
        st.session_state["evaluation"] = evaluation

if "analysis" in st.session_state:

    analysis = st.session_state["analysis"]

    st.markdown("---")
    st.subheader("🔍 Prompt Analysis")

    scores = [
        ("Quality", analysis.get("quality_score", 0)),
        ("Clarity", analysis.get("clarity", 0)),
        ("Specificity", analysis.get("specificity", 0)),
        ("Context", analysis.get("context", 0)),
        ("Constraints", analysis.get("constraints", 0)),
    ]

    cols = st.columns(5)

    for col, (name, score) in zip(cols, scores):
        col.metric(name, f"{score}/100")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            f"Ambiguity: **{analysis.get('ambiguity', 'Unknown').upper()}**"
        )

    with col2:
        st.warning(
            "Hallucination risk: **"
            + analysis.get("hallucination_risk", "Unknown").upper()
            + "**"
        )

    with col3:
        st.success("Analysis complete")

    left, right = st.columns(2)

    with left:
        st.subheader("⚠️ Issues Detected")

        for issue in analysis.get("issues", []):
            st.write("• " + str(issue))

        st.subheader("📌 Missing Information")

        missing = analysis.get("missing_information", [])

        if missing:
            for item in missing:
                st.write("• " + str(item))
        else:
            st.write("None detected")

    with right:

        recommendation = st.session_state.get(
            "recommendation",
            {}
        )

        st.subheader("🧠 Recommended Techniques")

        strategies = recommendation.get(
            "recommended_strategies",
            analysis.get("recommended_techniques", [])
        )

        for strategy in strategies:
            st.success("✓ " + str(strategy))

        if recommendation.get("primary_strategy"):
            st.info(
                "Primary recommendation: **"
                + recommendation["primary_strategy"]
                + "**"
            )

        st.subheader("💡 Why?")

        explanations = recommendation.get("explanations", [])

        for explanation in explanations:
            st.write("• " + str(explanation))

if "optimized" in st.session_state:

    st.markdown("---")
    st.subheader("✨ Prompt Optimization")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original Prompt")
        st.code(
            st.session_state["prompt"],
            language="text"
        )

    with col2:
        st.markdown("### Optimized Prompt")
        st.code(
            st.session_state["optimized"],
            language="text"
        )

if "original_response" in st.session_state:

    st.markdown("---")
    st.subheader("🤖 Response Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original Response")
        st.write(st.session_state["original_response"])

    with col2:
        st.markdown("### Optimized Response")
        st.write(st.session_state["optimized_response"])

if "evaluation" in st.session_state:

    st.markdown("---")
    st.subheader("📊 Evaluation")

    evaluation = st.session_state["evaluation"]

    if isinstance(evaluation, dict):

        metrics = [
            ("Original Score", evaluation.get("original_score", 0)),
            ("Optimized Score", evaluation.get("optimized_score", 0)),
            ("Improvement", evaluation.get("improvement", 0)),
        ]

        cols = st.columns(3)

        for col, (name, value) in zip(cols, metrics):
            col.metric(name, value)

        st.markdown("### Evaluation Details")

        for key, value in evaluation.items():
            if key not in {
                "original_score",
                "optimized_score",
                "improvement"
            }:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")

    else:
        st.write(evaluation)

elif not prompt.strip():
    st.info("Enter a prompt above to begin.")

st.markdown("---")
st.caption(
    "PromptGuard — Generative AI & Prompt Engineering Course Project"
)