import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="Indicateurs socio-économiques",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TITRE
# ============================================================

st.title("📊 Relations entre indicateurs socio-économiques")

st.write(
    """
    Cette activité permet d'étudier la relation entre deux indicateurs
    économiques ou sociaux pour différents pays.
    
    Choisissez deux variables puis cliquez sur **Afficher le graphique**.
    """
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data
def charger_donnees():

    es_vie = pd.read_csv(
        "esp_vie.csv",
        sep=";",
        decimal=","
    )

    irm = pd.read_csv(
        "IRM.csv",
        sep=";",
        decimal=","
    )

    scanners = pd.read_csv(
        "scanners.csv",
        sep=";",
        decimal=","
    )

    medecins = pd.read_csv(
        "medecins.csv",
        sep=";",
        decimal=","
    )

    education = pd.read_csv(
        "depense_education.csv",
        sep=";",
        decimal=","
    )

    cho = pd.read_csv(
        "tx_cho.csv",
        sep="\t",
        decimal=","
    )

    pib = pd.read_csv(
        "tx_pib_reel.csv",
        sep="\t",
        decimal=","
    )

    dette = pd.read_csv(
        "tx_dettepub.csv",
        sep=";",
        decimal=","
    )

    recherche = pd.read_csv(
        "R&D.csv",
        sep=";",
        decimal=","
    )

    brevets = pd.read_csv(
        "innovations.csv",
        sep=";",
        decimal=","
    )

    inflation = pd.read_csv(
        "inflation.csv",
        sep=";",
        decimal=","
    )

    productivite = pd.read_csv(
        "productivite.csv",
        sep=";",
        decimal=","
    )

    # Dictionnaire associant chaque code à son tableau
    dico = {
        "a": es_vie,
        "b": irm,
        "c": scanners,
        "d": medecins,
        "e": education,
        "f": cho,
        "g": pib,
        "h": dette,
        "i": recherche,
        "j": brevets,
        "k": inflation,
        "l": productivite
    }

    # Nom des variables affichées aux élèves
    inventaire = {
        "a": "Espérance de vie",
        "b": "Nombre d'IRM",
        "c": "Nombre de scanners",
        "d": "Nombre de médecins",
        "e": "Dépenses publiques d'éducation (% du PIB)",
        "f": "Taux de chômage",
        "g": "PIB",
        "h": "Dette publique (%)",
        "i": "Dépenses de R&D (% du PIB)",
        "j": "Brevets",
        "k": "Inflation",
        "l": "Productivité horaire"
    }

    return dico, inventaire


# ============================================================
# CHARGEMENT
# ============================================================

try:
    dico, inventaire = charger_donnees()

except Exception as erreur:

    st.error("❌ Une erreur est survenue lors du chargement des fichiers.")

    st.write("Détail de l'erreur :")
    st.code(str(erreur))

    st.stop()


# ============================================================
# CHOIX DES VARIABLES
# ============================================================

st.subheader("1️⃣ Choisissez deux variables")


noms_variables = list(inventaire.values())

colonne1, colonne2 = st.columns(2)


with colonne1:

    variable1_nom = st.selectbox(
        "Première variable",
        noms_variables,
        index=0
    )


with colonne2:

    variable2_nom = st.selectbox(
        "Deuxième variable",
        noms_variables,
        index=1
    )


# Retrouver les codes correspondant aux noms choisis

code1 = next(
    code for code, nom in inventaire.items()
    if nom == variable1_nom
)

code2 = next(
    code for code, nom in inventaire.items()
    if nom == variable2_nom
)


# ============================================================
# BOUTON
# ============================================================

st.divider()

afficher = st.button(
    "📈 Afficher le graphique",
    type="primary",
    use_container_width=True
)


# ============================================================
# GRAPHIQUE
# ============================================================

if afficher:

    if code1 == code2:

        st.warning(
            "⚠️ Vous devez choisir deux variables différentes."
        )

        st.stop()


    # --------------------------------------------------------
    # FUSION DES DEUX TABLEAUX
    # --------------------------------------------------------

    df1 = dico[code1].copy()
    df2 = dico[code2].copy()


    try:

        data = pd.merge(
            df1,
            df2,
            on="Pays",
            how="inner"
        )

    except Exception as erreur:

        st.error(
            "Impossible de fusionner les deux fichiers."
        )

        st.write(str(erreur))

        st.stop()


    # --------------------------------------------------------
    # IDENTIFICATION DES COLONNES DE DONNÉES
    # --------------------------------------------------------

    colonnes1 = [
        colonne for colonne in df1.columns
        if colonne != "Pays"
    ]

    colonnes2 = [
        colonne for colonne in df2.columns
        if colonne != "Pays"
    ]


    if len(colonnes1) == 0 or len(colonnes2) == 0:

        st.error(
            "Les fichiers CSV doivent contenir une colonne 'Pays' "
            "et au moins une colonne de données."
        )

        st.stop()


    colonne_x = colonnes1[0]
    colonne_y = colonnes2[0]


    # --------------------------------------------------------
    # CONVERSION EN NUMÉRIQUE
    # --------------------------------------------------------

    data[colonne_x] = pd.to_numeric(
        data[colonne_x],
        errors="coerce"
    )

    data[colonne_y] = pd.to_numeric(
        data[colonne_y],
        errors="coerce"
    )


    # Suppression des données manquantes

    data = data.dropna(
        subset=[colonne_x, colonne_y]
    )


    if len(data) < 2:

        st.error(
            "Il n'y a pas suffisamment de données communes "
            "pour réaliser le graphique."
        )

        st.stop()


    # --------------------------------------------------------
    # CALCUL DE LA CORRÉLATION
    # --------------------------------------------------------

    correlation = data[colonne_x].corr(
        data[colonne_y]
    )


    # --------------------------------------------------------
    # TITRE
    # --------------------------------------------------------

    st.subheader(
        f"Relation entre « {variable1_nom} » et « {variable2_nom} »"
    )


    st.write(
        f"Nombre de pays étudiés : **{len(data)}**"
    )


    # --------------------------------------------------------
    # GRAPHIQUE
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )


    sns.regplot(
        data=data,
        x=colonne_x,
        y=colonne_y,
        ax=ax,
        scatter_kws={
            "s": 70,
            "alpha": 0.75
        },
        line_kws={
            "color": "red",
            "linewidth": 2
        }
    )


    ax.set_xlabel(
        variable1_nom,
        fontsize=12
    )

    ax.set_ylabel(
        variable2_nom,
        fontsize=12
    )

    ax.set_title(
        f"{variable1_nom} et {variable2_nom}",
        fontsize=15,
        fontweight="bold"
    )


    ax.grid(
        alpha=0.25
    )


    st.pyplot(fig)


    # --------------------------------------------------------
    # COEFFICIENT DE CORRÉLATION
    # --------------------------------------------------------

    st.divider()

    st.subheader("📐 Coefficient de corrélation")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Corrélation",
            f"{correlation:.2f}"
        )


    with col2:

        if correlation > 0.7:
            interpretation = "Forte corrélation positive"

        elif correlation > 0.3:
            interpretation = "Corrélation positive"

        elif correlation > -0.3:
            interpretation = "Corrélation faible"

        elif correlation > -0.7:
            interpretation = "Corrélation négative"

        else:
            interpretation = "Forte corrélation négative"


        st.metric(
            "Interprétation",
            interpretation
        )


    with col3:

        st.metric(
            "Pays",
            len(data)
        )


    # --------------------------------------------------------
    # TABLEAU DES DONNÉES
    # --------------------------------------------------------

    with st.expander("🔎 Voir les données utilisées"):

        st.dataframe(
            data[
                ["Pays", colonne_x, colonne_y]
            ],
            use_container_width=True
        )


    # --------------------------------------------------------
    # RAPPEL POUR LES ÉLÈVES
    # --------------------------------------------------------

    st.info(
        """
        **Attention :** une corrélation entre deux variables ne signifie
        pas nécessairement qu'il existe une relation de causalité entre elles.

        Une corrélation positive signifie que les deux variables ont
        tendance à augmenter ensemble.

        Une corrélation négative signifie que lorsque l'une augmente,
        l'autre a tendance à diminuer.
        """
    )