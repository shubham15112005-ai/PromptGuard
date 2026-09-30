# PromptGuard 🛡️

**AI Prompt Quality & Optimization System**

PromptGuard is a Generative AI and Prompt Engineering course project that analyzes a user's prompt, identifies weaknesses, recommends prompting techniques, creates an optimized prompt, generates responses from the original and optimized prompts, and evaluates the difference between them.

## Core modules

1. **Prompt Analyzer** — scores clarity, specificity, context, and constraints; detects ambiguity and hallucination risk.
2. **Strategy Recommender** — recommends techniques such as role prompting, few-shot prompting, structured output, constraint prompting, context injection, decomposition, and self-critique.
3. **Prompt Optimizer** — rewrites the prompt while preserving the user's intent.
4. **Evaluation Engine** — compares original and optimized responses using relevance, clarity, completeness, and specificity.

## Stack

- Python
- Streamlit
- Groq API (OpenAI-compatible chat API)
- GPT-OSS 20B by default

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The app works in **Demo Mode** without an API key. For live GenAI mode, set `GROQ_API_KEY` in the environment or Streamlit secrets.

### Windows PowerShell

```powershell
$env:GROQ_API_KEY="your_key_here"
streamlit run app.py
```

## Deployment

The app is designed for Streamlit Community Cloud. Add the repository, set the `GROQ_API_KEY` secret, and deploy `app.py`.

**Never commit API keys.**

## Academic evaluation plan

Use a fixed test set of prompts covering academic, technical, creative, and analytical tasks. Run each prompt through the original and optimized paths, record the four evaluation criteria, and report averages. All numerical results in the final report should come from actual runs of this project.
