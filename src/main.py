from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Dict, Any

from agents.planner import PlannerAgent
from agents.explainer import ExplainerAgent
from agents.dataset_analyzer import analyze_dataset
from executor.executor import execute_plan
from schemas.plan_validator import validate_plan

# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------
app = FastAPI(title="AI Data Analyst Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = PlannerAgent()
explainer = ExplainerAgent()

# --------------------------------------------------
# HEALTH CHECK (HF SAFE)
# --------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# --------------------------------------------------
# HELPER
# --------------------------------------------------
def is_dataset_info_query(question: str) -> bool:
    keywords = [
        "dataset information",
        "dataset info",
        "describe dataset",
        "data overview",
        "summary of dataset",
        "about the dataset",
        "dataset summary"
    ]
    return any(k in question.lower() for k in keywords)

# --------------------------------------------------
# CORE LOGIC (USED BY FASTAPI + STREAMLIT)
# --------------------------------------------------
def analyze_dataframe(df: pd.DataFrame, question: str) -> Dict[str, Any]:
    """
    Core analysis pipeline.
    Streamlit IMPORTS and calls this directly.
    """

    # Dataset information
    if is_dataset_info_query(question):
        info_df = analyze_dataset(df)
        insight = explainer.explain_dataset(df)
        return {
            "type": "dataset_info",
            "table": info_df,
            "insight": insight
        }

    # Planner
    plan = planner.generate_plan(list(df.columns), question)

    # Validator
    validate_plan(plan, list(df.columns))

    # Executor
    result_df, _, _ = execute_plan(df, plan)

    # Explainer
    insight = explainer.explain(question, result_df, plan)

    return {
        "type": "analysis",
        "plan": plan,
        "results": result_df,
        "insight": insight
    }

# --------------------------------------------------
# FASTAPI ENDPOINT (OPTIONAL / LOCAL USE)
# --------------------------------------------------
@app.post("/analyze")
async def analyze(
    question: str = Form(...),
    file: UploadFile = File(...)
):
    df = pd.read_csv(file.file)
    result = analyze_dataframe(df, question)

    if result["type"] == "dataset_info":
        return {
            "type": "dataset_info",
            "table": result["table"].to_dict(orient="records"),
            "insight": result["insight"]
        }

    return {
        "type": "analysis",
        "plan": result["plan"],
        "results": result["results"].to_dict(orient="records"),
        "insight": result["insight"]
    }
