import streamlit as st
import pandas as pd
from openai import OpenAI

# ======================
# 🔒 PROTECTION
# ======================
if not st.session_state.get("auth", False):
    st.warning("Accès refusé")
    st.stop()

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="IA Data Analyst PRO", layout="wide")

st.title("📊 IA Data Analyst PRO")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ======================
# SESSION STATE
# ======================

if "history" not in st.session_state:
    st.session_state.history = []

if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = None

# ======================
# UPLOAD
# ======================

file = st.file_uploader("📂 Upload Excel", type=["xlsx"])

if file:
    st.session_state.df_loaded = pd.read_excel(file)

# ======================
# MAIN APP
# ======================

if st.session_state.df_loaded is not None:

    df = st.session_state.df_loaded

    st.subheader("🔍 Aperçu des données")
    st.dataframe(df)

    # ======================
    # MEMORY CONTEXT
    # ======================

    def get_memory_context():

        if not st.session_state.history:
            return "Aucun historique."

        context = ""

        for item in st.session_state.history[-5:]:
            context += f"User: {item['question']}\nAI: {item['answer']}\n\n"

        return context

    # ======================
    # IA FUNCTION
    # ======================

    def generate_result(question):

        memory_context = get_memory_context()

        prompt = f"""
Tu es un data analyst expert universel.

Historique :
{memory_context}

DONNÉES :
{df.to_string(index=False)}

COLONNES :
{df.columns.tolist()}

QUESTION :
{question}

RÉPONSE :
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Data analyst précis et business"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    # ======================
    # UI
    # ======================

    st.subheader("🧠 Pose ta question")

    question = st.text_input("Ex: Quel produit vend le plus ?")

    if st.button("Analyser"):

        if not question.strip():
            st.warning("Pose une question")
            st.stop()

        with st.spinner("Analyse en cours..."):
            result = generate_result(question)

        # ======================
        # SAVE MEMORY (SESSION ONLY)
        # ======================

        st.session_state.history.append({
            "question": question,
            "answer": result
        })

        st.subheader("📌 Résultat")
        st.write(result)

    # ======================
    # HISTORIQUE
    # ======================

    if st.session_state.history:

        st.subheader("🕘 Historique")

        for chat in reversed(st.session_state.history):

            st.write("🧑 Question :", chat["question"])
            st.write("🤖 Réponse :", chat["answer"])
            st.markdown("---")
