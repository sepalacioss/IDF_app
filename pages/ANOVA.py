import streamlit as st
import pandas as pd
import numpy as np
import itertools

import statsmodels.api as sm
from statsmodels.formula.api import ols

st.markdown('''
----
## Resultados para dos estaciones dentro de la misma cuenca
''')

st.sidebar.markdown('''
# Interpretación de Resultados de la Tabla ANOVA

Para interpretar los resultados de la tabla ANOVA en el contexto de este proyecto y comparar las intensidades calculadas con tres ecuaciones diferentes (`I1`, `I2`, `I3`), sigamos estos pasos:

## 1. Estructura de los datos:
- Tienes tres series de intensidades (`I1`, `I2`, `I3`) que fueron calculadas utilizando tres ecuaciones diferentes.
- Has transformado estos datos de un formato amplio a un formato largo usando la función `pd.melt()`. Esto te permite crear una columna llamada `Ecuacion`, que indica cuál de las ecuaciones fue utilizada para calcular la intensidad en cada fila, y una columna `Intensidad` que contiene los valores correspondientes de las intensidades.

## 2. Modelo ANOVA:
- El modelo que se construyó es un ANOVA de un solo factor, donde el factor es la ecuación usada `Ecuacion`.
- Este modelo evalúa si las diferencias en las intensidades calculadas por las tres ecuaciones (`I1`, `I2`, `I3`) son estadísticamente significativas.

## 3. Interpretación de la tabla ANOVA:
La tabla ANOVA te proporcionará varias métricas, pero las más relevantes son:

- **Sum of Squares (SS):** Indica la variabilidad de los datos que puede ser explicada por las diferencias entre las ecuaciones.
- **Degrees of Freedom (df):** El número de grados de libertad para el factor y el error residual.
- **Mean Square (MS):** Es el valor medio de los cuadrados (SS) dividido por los grados de libertad (df).
- **F-value:** Es la razón entre la variabilidad explicada por el modelo y la variabilidad residual. Un valor F más alto indica que las diferencias entre los grupos (en este caso, ecuaciones) son grandes en comparación con la variabilidad dentro de los grupos.
- **p-value:** Este es el valor clave para interpretar el resultado. Si el valor de `p` es menor que un umbral común (como 0.05), entonces hay evidencia estadística para rechazar la hipótesis nula, lo que significa que hay una diferencia significativa entre las intensidades calculadas por las diferentes ecuaciones.

## 4. Interpretación final:
- **Si el p-valor es pequeño (p < 0.05):** Puedes concluir que hay una diferencia significativa entre al menos una de las tres ecuaciones en términos de las intensidades que calculan. Esto significa que no todas las ecuaciones producen resultados similares y al menos una es significativamente diferente de las demás.
- **Si el p-valor es grande (p > 0.05):** No hay suficiente evidencia para concluir que las ecuaciones producen intensidades significativamente diferentes. Esto sugiere que todas las ecuaciones podrían estar calculando intensidades similares.
''')

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
st.markdown('''
----
## Análisis ANOVA entre estaciones de la misma cuenca
''')


col1,col2 = st.columns(2)

with col1:
    AnovaData1 = PrecData1[['I1','I2','I3']]
    AnovaData1 = pd.melt(AnovaData1.reset_index(), id_vars=['index'], value_vars=['I1', 'I2', 'I3'])
    AnovaData1.columns = ['index','Ecuacion','Intensidad']
    model1 = ols('Intensidad ~ C(Ecuacion)', data=AnovaData1).fit()
    anova_table1 = sm.stats.anova_lm(model1, typ=2)
    anova_table1

with col2:
    AnovaData2 = PrecData2[['I1','I2','I3']]
    AnovaData2 = pd.melt(AnovaData2.reset_index(), id_vars=['index'], value_vars=['I1', 'I2', 'I3'])
    AnovaData2.columns = ['index','Ecuacion','Intensidad']
    model2 = ols('Intensidad ~ C(Ecuacion)', data=AnovaData2).fit()
    anova_table2 = sm.stats.anova_lm(model2, typ=2)
    anova_table2
