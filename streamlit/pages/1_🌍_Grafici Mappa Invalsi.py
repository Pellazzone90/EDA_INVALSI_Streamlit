import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
import json

DATA_PATH = Path("data")
PERCORSO_IN = Path(DATA_PATH, "in")
PERCORSO_OUT = Path(DATA_PATH, "out")
GEOJSON_PATH = Path(PERCORSO_IN, "province.geojson")


df_pronto = pd.read_csv(
    Path(PERCORSO_OUT, "df_pronto.csv"),
    sep=",",
)

LISTA_MATERIE = df_pronto["materia"].unique().tolist()
LISTA_ANNI = tuple(set(df_pronto["anno"].values))
DICT_GRADI = {8:"III Media", 10:"II Superiore", 13:"V Superiore"}
LABEL_METRICHE =tuple(["Studenti sotto-media", "Studenti in-media", "Studenti sopra-media"])
LABEL_INGLESE_8 = tuple(["Livello Pre-A1", "Livello A1", "Livello A2"])
LABEL_INGLESE_13= tuple(["Non raggiunge il livello B1", "Livello B1", "Livello B2"])
DICT_METRICHE = {"Studenti sotto-media":"minore_95",
            "Studenti in-media":"95_110",
            "Studenti sopra-media":"maggiore_110",
            "Livello Pre-A1":"livello_1",
            "Livello A1":"livello_2",
            "Livello A2":"livello_3",
            "Non raggiunge il livello B1":"livello_1",
            "Livello B1":"livello_2",
            "Livello B2":"livello_3"
            }

def chloroplet_map_distribuzioni(geojson: json, df: pd.DataFrame, grado: int, metrica: str, label_metrica: str):
    if label_metrica in ["Studenti sotto-media", "Livello Pre-A1", "Non raggiunge il livello B1"]:
        fig = px.choropleth_mapbox(
            data_frame=df,
            geojson=geojson,
            locations="sigla_provincia",
            color=metrica,
            color_continuous_scale="rdbu_r",
            range_color=(df[metrica].min(), df[metrica].max()),
            mapbox_style="carto-positron",
            zoom=5,
            title=" Percentuale '{}' {} anno scolastico {}".format(label_metrica,option_grado,option_anno),
            center={"lat": 42, "lon": 12.5},
            opacity=0.5,
            labels={metrica:"Perc%"} 
        )
    else:
        fig = px.choropleth_mapbox(
            data_frame=df,
            geojson=geojson,
            locations="sigla_provincia",
            color=metrica,
            color_continuous_scale="rdbu",
            range_color=(df[metrica].min(), df[metrica].max()),
            mapbox_style="carto-positron",
            zoom=5,
            title="Percentuale '{}' {} anno scolastico {}".format(label_metrica,option_grado,option_anno),
            center={"lat": 42, "lon": 12.5},
            opacity=0.5,
            labels={metrica:"Perc."} 
        )
    fig.update_layout(height=780,
                    width=780,
                    margin=dict(l=0, r=200, t=30, b=0))
    return fig  
    
def chloroplet_map_rasch(geojson: json, dataframe: pd.DataFrame):
    fig = px.choropleth_mapbox(
            data_frame=dataframe,
            geojson=geojson,
            locations='sigla_provincia',
            color="punteggio_medio_wle",
            color_continuous_scale="rdbu",
            range_color=(dataframe["punteggio_medio_wle"].min(), dataframe["punteggio_medio_wle"].max()),
            #hover_data=['tot_sezioni', 'sezioni_corso', 'moda_volume', 'moda_editore'],
            mapbox_style="carto-positron",
            zoom=4.9, 
            center={"lat": 42, "lon": 12.5},
            opacity=0.5,
            title="Punteggio in '{}' {} anno scolastico {}".format(option_materia, option_grado, option_anno),
            labels={"punteggio_medio_wle":"Punteggio"}
            )
    fig.update_layout(height=780,
                    width=780,
                    margin=dict(l=0, r=200, t=30, b=0))
    return fig

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

with open(GEOJSON_PATH, 'r') as fp:
    geojson = json.load(fp)        
for feature_ in geojson['features']:
    feature_['id'] = feature_['properties']['SIGLA']



###########################################_APP STREAMLIT_###########################################

st.set_page_config(
    page_title="INVALSI", page_icon=":it:", layout="wide")

# Selezione parametri per il grafico:
option_anno = st.sidebar.select_slider(
    "Quale anno scolastico vuoi investigare?",
    sorted(LISTA_ANNI, reverse=False)
    )

option_materia = st.sidebar.selectbox(
    'Quale materia vuoi investigare?',
    sorted(LISTA_MATERIE, reverse=True)
    )

selezione = df_pronto[df_pronto["anno"].eq(option_anno) & \
                    df_pronto["materia"].eq(option_materia)]

LISTA_GRADI = selezione[selezione["materia"].eq(option_materia)]["grado"].unique().tolist()

option_grado = st.sidebar.radio(
    "Quale grado scolastico vuoi investigare?",
    tuple([DICT_GRADI[grado] for grado in LISTA_GRADI]))
option_grado_default = list(DICT_GRADI.keys())[list(DICT_GRADI.values()).index(option_grado)]


if "Inglese" not in option_materia:
    option_metrica = st.sidebar.selectbox(
        'Quale livello di abilità vuoi investigare?',
        LABEL_METRICHE
        )
    option_metrica_default = DICT_METRICHE[option_metrica]
else:
    if option_grado_default == 8:
        option_metrica = st.sidebar.selectbox(
            "Quale livello di inglese vuoi investigare?",
            LABEL_INGLESE_8
        )
        option_metrica_default = DICT_METRICHE[option_metrica]
    else:
        option_metrica = st.sidebar.selectbox(
            "Quale livello di inglese vuoi investigare?",
            LABEL_INGLESE_13
        )
        option_metrica_default = DICT_METRICHE[option_metrica]

#Fetch del dataframe per il grafico:
selezione = selezione[selezione["grado"].eq(option_grado_default)]

#Calcolo metriche da mostrare:
migliore_value = selezione[option_metrica_default].max()
migliore_provincia= selezione[selezione[option_metrica_default].eq(migliore_value)]["nome_provincia"].values[0]
peggiore_value = selezione[option_metrica_default].min()
peggiore_provincia = selezione[selezione[option_metrica_default].eq(peggiore_value)]["nome_provincia"].values[0]
rasch_migliore_value = selezione["punteggio_medio_wle"].max()
rasch_peggiore_value = selezione["punteggio_medio_wle"].min()
rasch_migliore_provincia = selezione[selezione["punteggio_medio_wle"].eq(rasch_migliore_value)]["nome_provincia"].values[0]
rasch_peggiore_provincia = selezione[selezione["punteggio_medio_wle"].eq(rasch_peggiore_value)]["nome_provincia"].values[0]

#Grafici:
grafico_distribuzioni = chloroplet_map_distribuzioni(geojson, selezione, option_grado_default, option_metrica_default, option_metrica)
grafico_rasch = chloroplet_map_rasch(geojson, selezione)

#Layout:
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
with tab1:
    tab1.title('Come si distribuiscono gli studenti per ogni provincia e con quale punteggio?:')
    col1, col2, col3= st.columns([3,0.4,3.2])
    with col1:
        if option_metrica in ["Livello Pre-A1", "Studenti sotto-media", "Non raggiunge il livello B1"]:
            col1.markdown(f"##### Provincia con la percentuale di studenti più alta:\
            \n ### {migliore_provincia} <font size='6' color='#FF0000'>{round(migliore_value,1)}%</font>\
            \n ##### Provincia con la percentuale di studenti più bassa:\
            \n ### {peggiore_provincia} <font size='6' color='#00FF00'>{round(peggiore_value,1)}%</font>",
            unsafe_allow_html=True
            )
        else:
            col1.markdown(f"##### Provincia con la percentuale di studenti più alta:\
            \n ### {migliore_provincia} <font size='6' color='#00FF00'> {round(migliore_value,1)}%</font>\
            \n ##### Provincia con la percentuale di studenti più bassa:\
            \n ### {peggiore_provincia} <font size='6' color='#FF0000'> {round(peggiore_value,1)}%</font>",
            unsafe_allow_html=True
            )
        st.markdown("------------------")
        st.subheader("**Mappa distribuzione studenti per provincia**:")
        st.plotly_chart(grafico_distribuzioni)
    with col3:
        col3.markdown(f"##### Provincia con il punteggio Rasch medio più alto:\
        \n ### {rasch_migliore_provincia} <font size='6' color='#00FF00'> {round(rasch_migliore_value,1)}</font>\
        \n ##### Provincia con il punteggio Rasch medio più basso:\
        \n ### {rasch_peggiore_provincia} <font size='6' color='#FF0000'> {round(rasch_peggiore_value,1)}</font>",
        unsafe_allow_html=True
        )
        st.markdown("------------------")
        st.subheader("**Mappa punteggio Rasch medio per provincia**:")
        st.plotly_chart(grafico_rasch)
with tab2:
    
    tab2.title('Dataframe sorgente ai grafici:')
    tab2.dataframe(selezione)
    selezione_csv = convert_df(selezione)
    st.download_button(
        label="Download Dataframe as CSV",
        data=selezione_csv,
        file_name=f'invalsi_{option_materia}_{option_anno}.csv',
        mime='text/csv'
    )