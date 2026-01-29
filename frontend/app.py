import streamlit as st
import pandas as pd
import requests

# ==================================================
# CONFIG
# ==================================================
BACKEND_URL = "http://localhost:8000/analyze"

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}

.card {
    background-color: white;
    padding: 1.25rem;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 1.2rem;
}

h1, h2, h3 {
    color: #1f2937;
}

div.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

div[data-testid="stAlert"] {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================
if "history" not in st.session_state:
    st.session_state.history = []

# ==================================================
# HEADER
# ==================================================
st.markdown("""
# 📊 AI Data Analyst Agent  
**Ask questions in plain English and get precise insights from your dataset.**

🔹 Upload any CSV  
🔹 Ask analytical questions  
🔹 Backend powered by FastAPI  
""")

st.divider()

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.header("📁 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    st.markdown("---")

    if st.button("🧹 Clear History"):
        st.session_state.history = []
        st.success("Session history cleared!")

# ==================================================
# MAIN CONTENT
# ==================================================
if uploaded_file:
    try:
        df_preview = pd.read_csv(uploaded_file, encoding="utf-8")
    except UnicodeDecodeError:
        df_preview = pd.read_csv(uploaded_file, encoding="latin1")

    # ---------------- Dataset Preview ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.expander("📋 Dataset Preview", expanded=True):
        st.dataframe(df_preview.head(20), use_container_width=True)
        st.caption(f"📊 Total: {df_preview.shape[0]:,} rows × {df_preview.shape[1]} columns")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Question Input ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Ask a Data Question")

    question = st.text_input(
        "",
        placeholder="e.g. Which country has the highest and lowest population?"
    )

    analyze_col, clear_col = st.columns([1, 1])

    with analyze_col:
        analyze_clicked = st.button("🚀 Analyze", use_container_width=True)

    with clear_col:
        if st.button("🧹 Clear Input"):
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ==================================================
    # ANALYSIS (API CALL)
    # ==================================================
    if analyze_clicked and question:
        try:
            with st.spinner("🚀 Sending request to backend..."):
                response = requests.post(
                    BACKEND_URL,
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

            # ---------------- DATASET INFO ----------------
            if data["type"] == "dataset_info":
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📄 Dataset Information")
                st.dataframe(pd.DataFrame(data["table"]), use_container_width=True)
                st.success("💡 Dataset Insights")
                st.markdown(data["insight"])
                st.markdown('</div>', unsafe_allow_html=True)
                st.stop()

            # ---------------- ANALYSIS RESULTS ----------------
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🧠 Analysis Plan")
            st.json(data["plan"])
            st.markdown('</div>', unsafe_allow_html=True)

            result_df = pd.DataFrame(data["results"])

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📊 Results")
            st.dataframe(result_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.success("💡 Key Insights")
            st.markdown(data["insight"])
            st.markdown('</div>', unsafe_allow_html=True)

            # ---------------- SAVE HISTORY ----------------
            st.session_state.history.append({
                "question": question,
                "plan": data["plan"],
                "result": result_df,
                "insight": data["insight"]
            })

        except Exception as e:
            st.error("❌ Failed to connect to backend")
            st.exception(e)

    # ==================================================
    # HISTORY
    # ==================================================
    if st.session_state.history:
        st.markdown("## 🕘 Analysis History")

        for idx, item in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"Query {idx}: {item['question']}"):
                st.markdown("**🧠 Analysis Plan**")
                st.json(item["plan"])

                st.markdown("**📊 Results**")
                st.dataframe(item["result"].head(10), use_container_width=True)

                st.markdown("**💡 Answer**")
                st.markdown(item["insight"])

else:
    st.info("👈 Upload a CSV file from the sidebar to begin analysis")
