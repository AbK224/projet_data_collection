from datetime import datetime
import streamlit as st
import base64
import pandas as pd
from bs4 import BeautifulSoup as bs
from db import create_table, get_connection
from scrapers.url1_chiens import scrap_dog_data
from scrapers.url2_moutons import scrap_sheeps_data
from scrapers.url3_pou_la_pi import scrap_animals_data
from scrapers.url4_autres import scrap_others_data
from cleaning import clean_data
from dashboard import show_dashboard




st.set_page_config(page_title="Projet Application de données Multi-sites",layout="wide")

#Ajouter une image en background
def set_background(image_file, target="main"):
    with open(image_file, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    if target == "main":
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
    elif target == "sidebar":
        css = f"""
        <style>
        section[data-testid="stSidebar"] {{
            background-image: url("data:image/png;base64,{img_data}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """

    st.markdown(css, unsafe_allow_html=True)
#Background page principale
set_background("assets/Capture d’écran 2026-02-25 221608.png", target="main")
#Background sidebar




st.markdown("<h1 style='text-align: center; color: #007BFF;'>Projet Application de données Multi-sites</h1>",unsafe_allow_html=True)

st.markdown("""
Cette application vous permet de télécharger les données scrappées relatives aux animaux 
* **Python libraries:** base64, pandas, streamlit,datetime,BeautifulSoup,webdriver,sqlite3
* **Data source:** https://sn.coinafrique.com.
* **Réalisé par:** **Abou Koné** etudiant en M1 à DIT
* *contact*: koneabou669@gmail.com
""")





  
#Initialisation des variables de session
if "scraping_done" not in st.session_state:
    st.session_state.scraping_done = False

if "data" not in st.session_state:
    st.session_state.data = {}



st.sidebar.title("Navigation")
nbre_pages = st.sidebar.number_input("Nombre de pages à scraper", min_value=1, max_value=50, value=1)

#menu deroulante
menu = st.sidebar.selectbox("Choisissez une action", 
                    ("Scrapper les données",
                      "Télécharger les données scrappées",
                      "Voir le dashboard",
                      "Evaluer l'application"
               ),placeholder="Choisissez une action",index=None)

#Navigation selon le choix    
if menu == "Scrapper les données":
    #Initialisation des variables de session
    # Fonction de loading des données
    def load_(dataframe, title, key) :
        st.markdown("""
        <style>
        div.stButton {text-align:center}
        </style>""", unsafe_allow_html=True)

        if st.button(title,key):
        
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)

    df1 = scrap_dog_data(nbre_pages)
    df1["date_scraped"] = datetime.now()
    
    
    df2 = scrap_sheeps_data(nbre_pages)
    df2["date_scraped"] = datetime.now()
   

    df3 = scrap_animals_data(nbre_pages)
    df3["date_scraped"] = datetime.now()


    df4 = scrap_others_data(nbre_pages)
    df4["date_scraped"] = datetime.now()
 
    df = pd.concat([df1, df2, df3, df4], ignore_index=True)
    st.session_state.data["df"] = df
    st.session_state.scraping_done = True 

    #stocker les donnees dans la base de donnees sql
    conn = get_connection()
    df.to_sql("animals_data", conn, if_exists="append", index=False)
    conn.close()
    st.success("Les données ont été enregistrées avec succès dans la base de données.")

    #Charger les donnees
    conn = get_connection()
    df_db = pd.read_sql("SELECT * FROM animals_data", conn)
    conn.close()
    
    # afficher boutons liées aux données
    load_(df1, "Afficher les données des chiens", "btn1")
    load_(df2, "Afficher les données des moutons", "btn2")
    load_(df3, "Afficher les données des poules, lapins et pigeons", "btn3")
    load_(df4, "Afficher les données des autres animaux", "btn4")
    load_(df_db, "Afficher les données depuis la base de données", "btn_db")

elif menu == "Télécharger les données scrappées":
    if st.session_state.get("scraping_done"):

        df = st.session_state.data.get("df")

        if df is not None:
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️Télécharger les données scrappées en CSV",
                data=csv,
                file_name="donnees_scrappees.csv",
                mime="text/csv",
            )
        else:
            st.warning("Aucune donnée disponible.")
    else:
        st.warning("Vous devez d'abord scraper les données.")

elif menu == "Voir le dashboard":
    if st.session_state.get("scraping_done"):
        df = st.session_state.data.get("df")
        if df is not None:
            df = clean_data(df)
            show_dashboard(df)
            st.markdown("### 📈 Nombre d’animaux par catégorie")

            # Récupération directe des DataFrames
            df1 = scrap_dog_data(nbre_pages)
            df2 = scrap_sheeps_data(nbre_pages)
            df3 = scrap_animals_data(nbre_pages)
            df4 = scrap_others_data(nbre_pages)

            # Comptage
            data_count = {
                "Chiens": len(df1),
                "Moutons": len(df2),
                "Poulets / Lapins / Pigeons": len(df3),
                "Autres animaux": len(df4),
            }

            count_df = pd.DataFrame.from_dict(
                data_count, orient="index", columns=["Nombre"]
            )

            
            st.bar_chart(count_df)
        else:
            st.warning("Aucune donnée disponible.")
    else:
        st.warning("Vous devez d'abord scraper les données.")

elif menu == "Evaluer l'application":
    st.subheader("Choisissez un formulaire d'évaluation")
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("Formulaire kobo", "https://ee.kobotoolbox.org/x/GsObLBeC")
    
    with col1:
        st.link_button("MS form", "https://docs.google.com/forms/d/e/1FAIpQLSczP0ywecRIDzypbh1poyOniI3EVZDAH-pcmu23EZIshN5qQA/viewform?usp=publish-editor")

    