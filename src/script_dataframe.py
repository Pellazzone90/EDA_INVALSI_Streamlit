import pandas as pd
import numpy as np
from pathlib import Path
import json

DATA_PATH = Path("..", "data")
PERCORSO_IN = Path(DATA_PATH, "in")
PERCORSO_OUT = Path(DATA_PATH, "out")

DTYPE_PROVINCE ={'Codice_provincia':int, 
    'Sigla_provincia':str, 
    'Nome_provincia':str, 
    'Grado':str,
    'Materia':str, 
    'Anno':str, 
    'LIVELLO_1':float, 
    'LIVELLO_2':float, 
    'LIVELLO_3':float, 
    'LIVELLO_4':float,
    'LIVELLO_5':float, 
    'perc_copertura_stu':float
                }

NA_VALUES_PROVINCE = {
    "Sigla_provincia": [""],
    "LIVELLO_1":["999"],
    "LIVELLO_2":["999"],
    "LIVELLO_3":["999"],
    "LIVELLO_4":["999"],
    "LIVELLO_5":["999"],
}

DTYPE_PUNTEGGI ={'Codice_provincia':int, 
    'Sigla_provincia':str, 
    'Nome_provincia':str, 
    'Grado':str,
    'Materia':str, 
    'Anno':str, 
    'punteggio_medio':float, 
    'deviazione_standard':float, 
    'punteggio_medio_wle':float, 
    'deviazione_standard_wle':float,
    'perc_copertura_stu':float
                }

NA_VALUES_PUNTEGGI = {
    "Sigla_provincia": [""],
    "punteggio_medio":["999"],
    "deviazione_standard":["999"],
    "punteggio_medio_wle":["999"],
    "deviazione_standard_wle":["999"],
    "perc_copertura_stu":["999"],
}

def generazione_dataframe() -> pd.DataFrame:
#caricamento dei datasets:
    df_province = pd.read_csv(
        Path(PERCORSO_IN, "Report_province_livelli.csv"),
        sep=";",
        decimal=",",
        dtype=DTYPE_PROVINCE,
        na_values=NA_VALUES_PROVINCE,
        keep_default_na=False
    )
    
    df_punteggi = pd.read_csv(
        Path(PERCORSO_IN, "Matrice_medie_provinciali.csv"),
        sep=";",
        decimal=",",
        dtype=DTYPE_PUNTEGGI,
        na_values=NA_VALUES_PUNTEGGI,
        keep_default_na=False
    )
#rinomino colonne:
    new_columns_province = {}
    for col in df_province.columns:
        new_col = col.lower().strip().replace(" ","_")
        new_columns_province[col] = new_col
        
    df_province = df_province.rename(columns=new_columns_province)
    
    new_columns_punteggi = {}
    for col in df_punteggi.columns:
        new_col = col.lower().strip().replace(" ","_")
        new_columns_punteggi[col] = new_col
    
    df_punteggi = df_punteggi.rename(columns=new_columns_punteggi)
    
#droppo i gradi delle scuole elementari, l'analisi si concentra solo sulle scuole medie e superiori:
    df_province = df_province.drop(df_province[df_province["grado"].isin(["5"])].index)
    df_punteggi = df_punteggi.drop(df_punteggi[df_punteggi["grado"].isin(["2", "5"])].index)

#fillo i nan con zero nelle colonne livello_4 e livello_5:
    df_province["livello_4"] = df_province["livello_4"].fillna(0)
    df_province["livello_5"] = df_province["livello_5"].fillna(0)
    
#rimuovo gli anni che non sono in comune e droppo le colonne vuote:
    anni_da_rimuovere = list(set(df_punteggi["anno"]) - set(df_province["anno"]))
    df_punteggi = df_punteggi.drop(df_punteggi[df_punteggi["anno"].isin(anni_da_rimuovere)].index)
    
    df_punteggi = df_punteggi.dropna(axis=1, how="all")
    
#definisco le colonne per il merge e mergio:
    colonne_sinistra = set(df_province.columns)
    colonne_destra = set(df_punteggi.columns)
    colonne_comuni = list(colonne_sinistra.intersection(colonne_destra))
    colonne_comuni.remove("perc_copertura_stu")
    colonne_comuni
    
    df = pd.merge(left=df_province,
                right=df_punteggi,
                on=colonne_comuni,
                how="left")
    
#creo le colonne per la codifica dei livelli:
    df["minore_95"] = round(df["livello_1"] + df["livello_2"],1)
    df["95_110"] = round(df["livello_3"],1)
    df["maggiore_110"] = round(df["livello_4"] + df["livello_5"],1)
    df["punteggio_medio_wle"] = round(df["punteggio_medio_wle"],1)

    return df

if __name__ == "__main__":
    
    df = generazione_dataframe()
    percorso_salvataggio = Path(PERCORSO_OUT)

    if percorso_salvataggio.exists():
        df.to_csv(
            str(percorso_salvataggio)+"/df_pronto.csv",
            index=False,
            )
    else:
        df.to_csv(
            str(percorso_salvataggio)+"/df_pronto.csv",
            index=False,
            )
