import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Indicateurs socio-économiques", layout="centered")

st.title("📊 Lien entre indicateurs socio-économiques")
st.caption(
    "Scanners et IRM : pour 1 000 000 d'habitants. "
    "Médecins : pour 1 000 habitants."
)

@st.cache_data
def charger_donnees():
    es_vie = pd.read_csv('esp_vie.csv', sep=';', decimal=',')
    irm = pd.read_csv('IRM.csv', sep=';', decimal=',')
    scanners = pd.read_csv('scanners.csv', sep=';', decimal=',')
    medecins = pd.read_csv('medecins.csv', sep=';', decimal=',')
    education = pd.read_csv('depense_education.csv', sep=';', decimal=',')
    cho = pd.read_csv("tx_cho.csv", sep="\t", decimal=",")
    pib = pd.read_csv("tx_pib_reel.csv", sep="\t", decimal=",")
    dette = pd.read_csv("tx_dettepub.csv", sep=";", decimal=",")
    recherche = pd.read_csv("R&D.csv", sep=";", decimal=",")
    brevets = pd.read_csv("innovations.csv", sep=";", decimal=",")
    inflation = pd.read_csv("inflation.csv", sep=";", decimal=",")
    productivite = pd.read_csv("productivite.csv", sep=";", decimal=",")

    cles = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l')
    variables = (
        'Esp_vie', 'IRM', 'Scanners', 'Medecins',
        'Depense_publique_education_%PIB', 'tx_cho', 'tx_pib_reel',
        'dette_publique_%', 'R&D_%PIB', 'Brevets', 'Inflation',
        'productivité_horaire'
    )
    valeurs = (
        es_vie, irm, scanners, medecins, education, cho, pib,
        dette, recherche, brevets, inflation, productivite
    )

    dico = {k: v for k, v in zip(cles, valeurs)}
    inventaire = {k: v for k, v in zip(cles, variables)}
    return dico, inventaire


try:
    dico, inventaire = charger_donnees()
except FileNotFoundError as e:
    st.error(
        f"Fichier introuvable : {e.filename}. "
        "Vérifie que tous les CSV sont bien présents à côté de app.py."
    )
    st.stop()

options = {f"{k} - {v}": k for k, v in inventaire.items()}

col1, col2 = st.columns(2)
with col1:
    choix_a = st.selectbox("Première variable", options.keys())
with col2:
    choix_b = st.selectbox("Deuxième variable", options.keys(), index=1)

a = options[choix_a]
b = options[choix_b]

if a == b:
    st.warning("Choisis deux variables différentes.")
    st.stop()

data = pd.merge(dico[a], dico[b], on='Pays', how='inner')

if data.empty:
    st.warning("Aucun pays commun entre ces deux jeux de données.")
    st.stop()

st.subheader(f"{inventaire[a]}  vs  {inventaire[b]}")

fig = sns.jointplot(x=inventaire[a], y=inventaire[b], data=data, kind='hex')
st.pyplot(fig.figure)

with st.expander("Voir les données utilisées"):
    st.dataframe(data)
