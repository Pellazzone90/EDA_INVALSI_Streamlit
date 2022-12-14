import pandas as pd
import streamlit as st
import plotly.express as px
import json
import numpy as np

from pathlib import Path
from PIL import Image

DATA_PATH = Path("data")
PERCORSO_IN = Path(DATA_PATH, "in")
PERCORSO_OUT = Path(DATA_PATH, "out")

#MORANI = Image.open(Path(PERCORSO_IN,"immagini","moranI.png"))
LISA_RASCH = Image.open(Path(PERCORSO_IN,"LISA_punteggio_medio_wle.png"))

###########################################_APP STREAMLIT_###########################################
st.set_page_config(
    page_title="INVALSI", page_icon=":it:", layout="wide")

###############################################LAYOUT APP###############################################À

#tabs:
tab1 = st.tabs(["📈 Chart"])

st.title("La distribuzione spaziale degli studenti è casuale?")
col1, col2, col3= st.columns([3,0.1,3.0])
col1.markdown("##### Punteggio medio Rasch Matematica V Liceo 2020-21:")
col1.image(LISA_RASCH)
col1.markdown("------------------")
st.markdown(
    f"Le conclusioni qui presentate sono state ottenute tramite l'analisi statistica geospaziale **LISA**,\
    un algoritmo sviluppato per identificare e localizzare cluster spaziali autocorrelati. \
    \
    \n \
    \nL'immagine riportata contenente quattro mappe, mostra il livello di significatività per l'autocorrelazione spaziale nella distribuzione\
    del **punteggio di Rasch medio** sul territorio nazionale.\
    \n Poniamo particolare attenzione alle mappa in basso negli angoli sinistro e destro. \
    \n In esse possiamo notare la presenza di 2 *cluster* che separano chiaramente il **Nord** dal **Sud** del paese.\
    \n\
    \n **Province con punteggi più alti (studenti più abili) si concentrano tra loro vicine e altrettanto fanno le province con punteggi più bassi (studenti meno abili).**\
    \n \
    \n Il modo in cui gli studenti si localizzano non è casuale! \
    \n Da quanto appare nei grafici così ottenuti, la distribuzione degli studenti migliori si concentra nel Nord Italia,\
    \n sembra evidente il manifestarsi di quel classico divario Nord-Sud che da anni caratterizza il *Belpaese!*"
    )