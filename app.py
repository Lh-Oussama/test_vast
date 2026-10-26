import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Test Vast", page_icon="🚀")

st.title("🚀 Test Streamlit sur Vast.ai")
st.write("Interface simple pour vérifier que Streamlit fonctionne.")

# --- Interaction de base ---
nom = st.text_input("Ton prénom", "")
if nom:
    st.success(f"Bonjour {nom} !")

# --- Slider + graphique ---
n = st.slider("Nombre de points", min_value=10, max_value=500, value=100)
data = pd.DataFrame(np.random.randn(n, 2), columns=["a", "b"])
st.line_chart(data)

# --- Bouton ---
if st.button("Afficher un tableau"):
    st.dataframe(data.describe())

# --- Infos GPU (PyTorch) ---
st.subheader("Machine")
try:
    import torch

    if torch.cuda.is_available():
        st.write("GPU :", torch.cuda.get_device_name(0))
    else:
        st.write("Pas de GPU détecté (CPU seulement).")
except ImportError:
    st.write("PyTorch non installé.")