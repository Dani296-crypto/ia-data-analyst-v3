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
# CONFIG OPENAI
# ======================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ======================
# HISTORIQUE
# ======================
if "history" not in st.session_state:
    st.session_state.history = []

# ======================
# UPLOAD
# ======================
file = st.file_uploader("📂 Upload Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file)

    st.dataframe(df)

    def generate_result(question):
        prompt = f"""
Tu es un data analyst expert.

Données:
{df.to_string(index=False)}

Question:
{question}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Data analyst précis"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    question = st.text_input("Question")

    if question:
        result = generate_result(question)

        st.session_state.history.append({
            "question": question,
            "answer": result
        })

        st.write(result)

    for chat in reversed(st.session_state.history):
        st.write(chat)
