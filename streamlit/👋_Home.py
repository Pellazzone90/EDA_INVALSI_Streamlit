import streamlit as st


st.set_page_config(
    page_title="INVALSI",
    page_icon=":it:",
    layout="wide"
)
st.write("# Visualizzazione geospaziale dati prove INVALSI")
st.markdown("------")
st.markdown(
    """
    In questo applicativo vengono analizzati i dati INVALSI forniti dal Cineca [Link](https://invalsi-serviziostatistico.cineca.it/)

    I dati fanno riferimento alle prove svoltesi tra il 2017 ed il 2021 ad esclusione dell'anno scolastico 2019-2020.\
    \n Le materie delle prove sono **Matematica**, **Italiano**, **Inglese R**(Lettura) ed **Inglese L**(ascolto) declinate per i seguenti gradi:\
    \n -III secondaria di I grado, **III Media**\
    \n -II secondaria di II grado, **II Superiore**\
    \n -V secondaria di II grado, **V Superiore**\
    \n **NB** Nella selezione del grado scolastico di riferimento uno o più valori possono essere assenti se, per lo specifico anno e materia, le prove INVALSI non si sono tenute.
    
    Per ogni materia e per ogni grado scolastico gli studenti vengono divisi in **3 livelli di abilità**. Di ogni livello viene calcolata la percentuale di studenti che vi appartiene.\
    \n I livelli di abilità vengono definiti in funzione del *punteggio di Rasch medio* che, per ogni materia e grado scolastico, gli studenti di ogni provincia totalizzano rispetto al valore di media nazionale.\
    Sulla scala INVALSI la media nazionale per il *punteggio di Rasch* è posto a **200**.\n
    \n Il *Punteggio di Rasch* valuta su una scala di abilità la preparazione degli studenti in funzione della difficoltà delle prove.\

    👈 Tramite **Grafici Mappa Invalsi** possiamo visualizzare la distribuzione degli studenti sul territorio nazionale.\
    \n ### Cosa visualizzeremo?
    La pagina **Grafici Mappa Invalsi** presenta 2 Tab\

        \n Tab 📈 Chart:
    - **KPI** per la provincia *migliore* e *peggiore*
    - **Mappa** distribuzione percentuali studenti per livello di abilità (**sinistra**)
    - **Mappa** distribuzione punteggio di *Rasch* (**destra**)
    Tab 🗃 Data:
    - **Dataframe** sorgente dati per i grafici\
"""
)