import streamlit as st
import pandas as pd
import numpy as np
import itertools

df = pd.read_csv("pages/Data_downloaded.csv")
df['Fecha'] = pd.to_datetime(df['fechaobservacion'])
df.drop(columns='fechaobservacion',inplace=True)

def eq1(T, t, M):
    a, b, c, D = 2.16,0.19,0.62,0.62
    return a * (T**b) / (t**c) * (M**D)

def eq2(T, t, M, N):
    a, b, c, D, E =  2.83, 0.19,0.62,0.62,-0.04
    return a * (T**b) / (t**c) * (M**D) * (N**E)

def eq3(T, t, M, N, PT):
    a, b, c, D, E, f = 3.87, 0.19,0.62,0.35,-0.33,0.32
    return a * (T**b) / (t**c) * (M**D) * (N**E) * (PT**f)

def eq4(T, t, M, N, PT, ELEV):
    a, b, c, D, E, f, g = 3.69, 0.19,0.62,0.32,-0.23,0.30,-0.03
    return a * (T**b) / (t**c) * (M**D) * (N**E) * (PT**f) * (ELEV**g)

col1, col2 = st.columns(2)

with col1:
    station1 = st.selectbox(
        "Seleccione la 1er estacion a visualizar",
        df["nombreestacion"].unique()
    )
    
    ndf = df.loc[df['nombreestacion'] == station1]
    ndf.sort_index(inplace=True)
    prec_diario = ndf.resample('D', on = 'Fecha').sum()
    
    df_anual_max = prec_diario['valorobservado'].resample('Y').max()
    M = np.round(np.mean(df_anual_max.values),2)
    
    dias_con_lluvia = prec_diario[prec_diario['valorobservado'] > 0].shape[0]
    N = np.round(dias_con_lluvia / (len(prec_diario) / 365),0)
    
    df_anual = prec_diario['valorobservado'].resample('Y').sum()
    PT = np.round(np.mean(df_anual.values),2)
    
    
    times = np.linspace(1,60,50)
    Frequencies = [2,5,10,20,50,100]
    DF = []
    new_rows = []
    for t in times:
        for T in Frequencies:
            new_row = []
            I1 = eq1(T,t,M)
            I2 = eq2(T,t,M,N)
            I3 = eq3(T,t,M,N,PT)
            new_row = {'I1':I1,'I2':I2,'I3':I3,'t':t,'T':T}
            new_rows.append(new_row)
    DF.append(new_rows)
    PrecData1 = pd.DataFrame(list(itertools.chain.from_iterable(DF)))
    
    PrecData1

with col2:
    station2 = st.selectbox(
        "Seleccione la 2da estacion a visualizar",
        df["nombreestacion"].unique()
    )
    
    ndf = df.loc[df['nombreestacion'] == station2]
    ndf.sort_index(inplace=True)
    prec_diario = ndf.resample('D', on = 'Fecha').sum()
    
    df_anual_max = prec_diario['valorobservado'].resample('Y').max()
    M = np.round(np.mean(df_anual_max.values),2)
    
    dias_con_lluvia = prec_diario[prec_diario['valorobservado'] > 0].shape[0]
    N = np.round(dias_con_lluvia / (len(prec_diario) / 365),0)
    
    df_anual = prec_diario['valorobservado'].resample('Y').sum()
    PT = np.round(np.mean(df_anual.values),2)
    
    
    times = np.linspace(1,60,50)
    Frequencies = [2,5,10,20,50,100]
    DF = []
    new_rows = []
    for t in times:
        for T in Frequencies:
            new_row = []
            I1 = eq1(T,t,M)
            I2 = eq2(T,t,M,N)
            I3 = eq3(T,t,M,N,PT)
            new_row = {'I1':I1,'I2':I2,'I3':I3,'t':t,'T':T}
            new_rows.append(new_row)
    DF.append(new_rows)
    PrecData2 = pd.DataFrame(list(itertools.chain.from_iterable(DF)))
    
    PrecData2
