import streamlit as st

if "auth" not in st.session_state or not st.session_state["auth"]:
    st.stop()
    
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os

# ======================
# INIT HISTORIQUE
# ======================
if "history" not in st.session_state:
    st.session_state.history = []

# ======================
# UPLOAD
# ======================
file = st.file_uploader("📂 Upload Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file)

    st.subheader("🔍 Aperçu des données")
    st.dataframe(df)

    # ======================
    # IA FUNCTION
    # ======================
    def generate_result(question):

        prompt = f"""
Tu es un data analyst expert universel.

MISSION :
Analyser n'importe quel fichier Excel et répondre aux questions utilisateur.

RÈGLES ABSOLUES :
- Tu ne supposes aucune colonne
- Tu utilises uniquement les données fournies
- Tu fais les calculs directement à partir du tableau
- Tu réponds même si le dataset est différent à chaque fois
- Tu ne demandes jamais de confirmation
- Si une information est absente, tu dis "non disponible"
- Tu adaptes ton analyse selon les données

DONNÉES COMPLETES DU FICHIER :
{df.to_string(index=False)}

COLONNES DETECTÉES :
{df.columns.tolist()}

QUESTION UTILISATEUR :
{question}

RÉPONSE :
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un data analyst universel précis, logique et orienté business."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    # ======================
    # UI
    # ======================
    st.subheader("🧠 Pose ta question")

    question = st.text_input("Ex: Analyse ce fichier et donne-moi les insights")

    if question:
        with st.spinner("Analyse en cours... 🤖"):
            result = generate_result(question)

        # ======================
        # HISTORIQUE
        # ======================
        st.session_state.history.append({
            "question": question,
            "answer": result
        })

        st.subheader("📊 Résultat Data Analyst")
        st.write(result)

    # ======================
    # AFFICHAGE HISTORIQUE
    # ======================
    if st.session_state.history:
        st.subheader("💬 Historique Conversation")

        for chat in reversed(st.session_state.history):
            st.markdown("---")
            st.write("🧑 Question :", chat["question"])
            st.write("🤖 Réponse :", chat["answer"])
