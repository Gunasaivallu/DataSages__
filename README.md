---
title: AI Data Analyst Agent
emoji: 📊
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---





# 📊 AI Data Analyst Agent for CSV-Based Analysis

**Employee Name:** Gunasaivallu

---

## 1. Research Question / Hypothesis

Can a **Planner–Validator–Executor–Explainer architecture**, powered by Large Language Models (LLMs), enable **safe, reproducible, and structured analysis of CSV datasets**, while preventing hallucinated computations and non-deterministic execution commonly observed in end-to-end LLM data analysis systems?

---

## 2. Motivation and Relevance

Large Language Models are increasingly used for data analysis tasks. However, many existing systems:

- Hallucinate numerical results  
- Generate unverifiable reasoning steps  
- Directly execute LLM-generated code on user data  
- Produce non-reproducible outputs  

These issues pose significant risks in analytical and decision-making contexts.

This project addresses these challenges by enforcing a **strict separation between reasoning and execution**, ensuring that:

- LLMs are used **only for planning and explanation**
- All numerical computations are performed **deterministically using pandas**
- Every analytical step is **validated before execution**

This design significantly improves **trustworthiness, safety, and reproducibility**.

---

## 3. System Architecture

The system is implemented as a **two-tier architecture** consisting of a Streamlit frontend and a FastAPI backend, connected via a REST API.

### Architectural Flow
```
  User (Streamlit UI)
          ↓
FastAPI Backend (`/analyze`)
          ↓
  Planner Agent (LLM)
          ↓
Plan Validator (Schema Enforcement)
          ↓
Executor (Deterministic pandas Execution)
          ↓
  Explainer Agent (LLM)
          ↓
Structured Results + Natural Language Insights
          ↓
  Streamlit UI Display
```


### Key Architectural Principle

> **LLMs never perform numerical computation.**  
> All calculations are executed deterministically using pandas after schema validation.

---

## 4. Model(s) and Versions Used

- **Large Language Model:** Groq-hosted LLM  
- **Usage Scope:**
  - Planner Agent → generates structured analysis plans  
  - Explainer Agent → generates natural language explanations  
- **Execution Engine:** pandas (Python)  
- **Backend Framework:** FastAPI  
- **Frontend Framework:** Streamlit  

The executor and validator layers are entirely **LLM-independent**.

---

## 5. Prompting and/or Fine-Tuning Strategy

### Prompting Strategy

#### Planner Agent
- Receives dataset column names and the user question  
- Produces a structured, machine-readable analysis plan (JSON)  
- Explicitly constrained to allowed operations  

#### Explainer Agent
- Receives execution results and the validated plan  
- Generates descriptive, human-readable insights  
- **Forbidden from generating numerical values**

### Fine-Tuning

- No fine-tuning was performed  
- The system relies on **prompt constraints and architectural enforcement** rather than model retraining

---

## 6. Evaluation Protocol

The system was evaluated using multiple CSV datasets and analytical queries, focusing on:

- Numerical correctness of results  
- Absence of hallucinated values  
- Schema validation effectiveness  
- Reproducibility across repeated runs  
- Explainability of outputs  

Dataset overview queries (e.g., *“Describe the dataset”*) were evaluated separately to ensure correct routing without invoking the planner–executor pipeline.

---

## 7. Key Results

- ✅ Zero hallucinated numerical outputs  
- ✅ Fully deterministic and reproducible execution  
- ✅ Clear reasoning trace via structured analysis plans  
- ✅ Safe handling of arbitrary CSV files  
- ✅ Improved interpretability through explicit explanations  

*(Results are derived from system execution logs and evaluation notebooks in the `notebooks/` directory.)*

---

## 8. Known Limitations and Ethical Considerations

### Known Limitations
- Supports only CSV file format  
- Single-table analysis only  
- In-memory execution limits scalability for very large datasets  
- Limited visualization support (tabular outputs only)  

### Ethical Considerations
- No training or storage of user data  
- No external data sources accessed  
- Deterministic execution prevents misleading or fabricated results  
- User datasets remain session-scoped  

---

## 9. Exact Instructions to Reproduce Results

### 1️⃣ Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
### 2️⃣ Environment Variables

Create a `.env` file using `.env.example`:

```env
GROQ_API_KEY=your_api_key_here
```

### 3️⃣ Start Backend (FastAPI)

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 4️⃣ Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

### 5️⃣ Usage

- Upload a CSV file  
- Ask a natural language analytical question  
- View:
  - Generated analysis plan  
  - Deterministic results  
  - Natural language explanation  

### 6️⃣ Optional: Docker

```bash
docker build -t ai-data-analyst .
docker run -p 8000:8000 ai-data-analyst
```

## Appendix A: Project Structure

```text
Datasages/
│
├── data/                       # Sample CSV datasets
│   ├── Book1.csv
│   └── population_by_country_2020.csv
│
├── experiments/                # Experiment configurations
│   ├── exp_01.yaml
│   └── exp_02.yaml
│
├── frontend/
│   ├── __init__.py
│   └── app.py                  # Streamlit UI
│
├── notebooks/                  # Exploration & evaluation notebooks
│   ├── 01_exploration.ipynb
│   └── 02_evaluation.ipynb
│
├── src/
│   ├── agents/
│   │   ├── planner.py          # LLM-based planner
│   │   ├── explainer.py        # LLM-based explainer
│   │   └── dataset_analyzer.py # Dataset summary logic
│   │
│   ├── executor/
│   │   └── executor.py         # Deterministic pandas execution
│   │
│   ├── schemas/
│   │   └── plan_validator.py   # Plan validation rules
│   │
│   ├── utils/
│   │   └── __init__.py
│   │
│   ├── config.py               # Model & environment config
│   └── main.py                 # FastAPI backend entry point
│
├── Dockerfile
├── requirements.txt
├── project.yaml
├── reproducibility.md
├── .env.example
└── README.md

```
