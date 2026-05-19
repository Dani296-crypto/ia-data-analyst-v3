import streamlit as st

st.set_page_config(page_title="Login IA", layout="centered")

# INIT STATE
if "auth" not in st.session_state:
    st.session_state["auth"] = False

# SI DEJA CONNECTE → aller dashboard
if st.session_state["auth"]:
    st.switch_page("ia")
    st.stop()

st.title("🔐 Login")

password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):

    if password == st.secrets["APP_PASSWORD"]:
        st.session_state["auth"] = True
        st.success("Accès autorisé")
        st.switch_page("ia")

    else:
        st.error("Mot de passe incorrect")
