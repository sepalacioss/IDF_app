import streamlit as st
import seaborn as sns
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.sidebar.markdown("En esta página se pueden visualizar las curvas IDF generadas con las diferentes ecuaciones, para las diversas estaciones disponibles en el área de estudio")

st.markdown('''
# Seleccion de la estacion de interes a evaluar
            
Los datos descargados de las estaciones ubicadas dentro del poligono de interes de la cuenca se muestran para cada estacion a continuacion:          
''')

df = pd.read_csv("pages/Data_downloaded.csv")
df['Fecha'] = pd.to_datetime(df['fechaobservacion'])
df.drop(columns='fechaobservacion',inplace=True)

station = st.selectbox(
    "Seleccione la estacion a visualizar",
    df["nombreestacion"].unique()
)

ndf = df.loc[df['nombreestacion'] == station]
ndf.sort_index(inplace=True)
prec_diario = ndf.resample('D', on = 'Fecha').sum()
fig, ax = plt.subplots()
prec_diario['valorobservado'].plot(ax = ax)

st.pyplot(fig)

st.markdown('''___
## Construcción de curvas IDF usando las ecuaciones 
Para la construcción de las curvas IDF se usan las ecuaciones que se muestran a continuación 
            ''')


st.latex(r'''
    \begin{equation}
    I = a\frac{T^b}{t^c}M^D
    \end{equation}\\[2mm]
    \begin{equation}
    I = a\frac{T^b}{t^c}M^DN^E
    \end{equation}\\[2mm]

    \begin{equation}
     I = a\frac{T^b}{t^c}M^DN^EPT^f
    \end{equation} \\[2mm]
   
    \begin{equation}
    \displaystyle I = a\frac{T^b}{t^c}M^DN^EPT^fELEV^g
    \end{equation}
         ''')

st.markdown('''
___
### Definición de los parámetros
Para la estimación de los parámetros necesarios a usar en la ecuaciones tenemos que:            
            ''')

df_anual_max = prec_diario['valorobservado'].resample('Y').max()
M = np.round(np.mean(df_anual_max.values),2)

dias_con_lluvia = prec_diario[prec_diario['valorobservado'] > 0].shape[0]
N = np.round(dias_con_lluvia / (len(prec_diario) / 365),0)

df_anual = prec_diario['valorobservado'].resample('Y').sum()
PT = np.round(np.mean(df_anual.values),2)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### M: Promedio precip máxima 24 hr (mm)")
    M

with col2:
    st.markdown("#### N: promedio de días con lluvia al año")
    N

with col3:
    st.markdown("#### P T: Precipitación media anual (mm)")
    PT


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
PrecData = pd.DataFrame(list(itertools.chain.from_iterable(DF)))
# PrecData

st.markdown('''
___
### Construcción de curvas IDF
            ''')

ecuacion = st.selectbox(
    "Seleccione la ecuación a utilizar",
    [1,2,3,4]
)
Ieq = 'I'+str(ecuacion)
# Ieq

fig, ax = plt.subplots()

sns.lineplot(data = PrecData[[Ieq,'t','T']],x = 't', y = Ieq , ax = ax, hue = 'T')
ax.set_xlabel("Duración (min)")
ax.set_ylabel("Intensidad (mm)")
ax.set_title(f"IDF a partir de la ecuación {ecuacion}")
ax.legend(title="Periodo de retorno \n (años)")

st.pyplot(fig)

