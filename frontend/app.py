import streamlit as st
import pandas as pd
import requests

# ------------------------------
# CONFIG (LOCALHOST)
# ------------------------------
BACKEND_URL = "http://localhost:8000/analyze"

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)

# ------------------------------
# SESSION STATE
# ------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------
# HEADER
# ------------------------------
st.title("📊 AI Data Analyst Agent")
st.caption("Ask questions in plain English and get insights from your CSV")

# ------------------------------
# SIDEBAR
# ------------------------------
with st.sidebar:
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if st.button("🧹 Clear History"):
        st.session_state.history = []
        st.success("History cleared")

# ------------------------------
# MAIN
# ------------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    question = st.text_input(
        "Ask a data question",
        placeholder="e.g. Which country has the highest population?"
    )

    if st.button("🚀 Analyze") and question:
        with st.spinner("Sending request to backend..."):

            # ✅ EXACT REQUEST YOU ASKED FOR
            response = requests.post(
                "http://localhost:8000/analyze",
                data={"question": question},
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )
                },
                timeout=300
            )

        if response.status_code != 200:
            st.error("❌ Backend error")
            st.text(response.text)
            st.stop()

        data = response.json()

        if data["type"] == "dataset_info":
            st.subheader("📄 Dataset Information")
            st.dataframe(pd.DataFrame(data["table"]))
            st.success(data["insight"])
            st.stop()

        st.subheader("🧠 Analysis Plan")
        st.json(data["plan"])

        result_df = pd.DataFrame(data["results"])
        st.subheader("📊 Results")
        st.dataframe(result_df)

        st.success(data["insight"])

        st.session_state.history.append({
            "question": question,
            "plan": data["plan"],
            "result": result_df,
            "insight": data["insight"]
        })

# ------------------------------
# HISTORY
# ------------------------------
if st.session_state.history:
    st.markdown("## 🕘 Analysis History")
    for item in reversed(st.session_state.history):
        with st.expander(item["question"]):
            st.json(item["plan"])
            st.dataframe(item["result"])
            st.markdown(item["insight"])
