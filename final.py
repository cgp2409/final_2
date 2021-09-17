# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:48:38 2021

@author: cgp24
"""

# Importar paquetes
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64

st.markdown("<h1 style='text-align: center; color: #3C9AD0;'> Hurtos en medellín y Neiva </h1>", unsafe_allow_html=True)

# Función para importar datos
#@st.cache(persist=True) # Código para que quede almacenada la información en el cache
def load_data1(url):
    df = pd.read_csv(url) # leer datos
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho']) # convertir fecha a formato fecha    
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'], format='%Y:%m:%d:%H:%M:%S') # convertir hora a formato fecha
    df['YEAR'] = df['fecha_hecho'].dt.year # sacar columna con año
    df['DAY'] = df['fecha_hecho'].dt.strftime('%a')
    df['MONTH']=df['fecha_hecho'].dt.month
    df.columns = df.columns.map(str.lower) # convertir columnas a minúscula
    df['hurtos'] = 1
    
    return df
hm = load_data1('hm.csv')
def load_data2(url):
    df = pd.read_csv(url) # leer datos
    df['fecha_del_hecho'] = pd.to_datetime(df['fecha_del_hecho']) # convertir fecha a formato fecha    
    df['fecha_del_hecho'] = pd.to_datetime(df['fecha_del_hecho'], format='%Y:%m:%d:%H:%M:%S') # convertir hora a formato fecha
    df['YEAR'] = df['fecha_del_hecho'].dt.year # sacar columna con año
    df['DAY'] = df['fecha_del_hecho'].dt.strftime('%a')
    df['MONTH']=df['fecha_del_hecho'].dt.month
    df.columns = df.columns.map(str.lower) # convertir columnas a minúscula
    df['hurtos'] = 1
    
    return df
hn1 = load_data2('hn.csv')
hn1 = hn1.rename(columns ={'género':'sexo','rango_edad':'rango_edad','comuna/corregimiento':'comuna','barrio/vereda':'nombre_barrio','arma-medio':'arma_medio','clase_de_sitio':'lugar'})
hn = hn1.rename(columns ={'rango-edad':'rango_edad'})
dfunion = load_data1('dfunion.csv')
c1, c2 = st.columns([1,1])



# 1.¿Cuáles son las características más comunes de la poblacion victima de hurtos (Rango de edad y sexo)? medellín
#medellin
c1.markdown("<h3 style='text-align: center; color: black;'>Sexo y edad de las victimas </h3>", unsafe_allow_html=True)
g1 = hm.groupby(['sexo','rango_edad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="rango_edad", y="hurtos", color="sexo", title="Sexo y edad de las victimas Medellín")
fig.update_layout(xaxis_title="<b>Rango de edad<b>",
                  yaxis_title="<b>Edades<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')
c1.write(fig)
#neiva
c2.markdown("<h3 style='text-align: center; color: black;'>Sexo y edad de las victimas </h3>", unsafe_allow_html=True)

g2 = hn.groupby(['sexo','rango_edad'])[['hurtos']].count().reset_index()
fig = px.bar(g2, x="rango_edad", y="hurtos", color="sexo", title="Sexo y edad de las victimas neiva")
fig.update_layout(xaxis_title="<b>Rango de edad<b>",
                  yaxis_title="<b>Edades<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')
c2.write(fig)





# 2.¿Cuales son las comunas con mayor poblacion victima de hurtos ? medellín
#medellin
#este podria hacer lo de los exagonos que salen**
c1.markdown("<h3 style='text-align: center; color: black;'>Victimas por comuna Medellín</h3>", unsafe_allow_html=True)

token_map = 'pk.eyJ1IjoiZGllZ29iYXJjbzUiLCJhIjoiY2txd3pvNm81MG84YzJubnoxbWg2MHY1aSJ9.UVtLXyahSUtwEIvS49B_hg'
px.set_mapbox_access_token(token_map)
lista = hm['comuna'].value_counts().index
#[hm['codigo_comuna'].value_counts()<20]
hurtos = hm[hm['comuna'].isin(lista)] 
#.dropna(subset = ['codigo_comuna'])
#quitar  valores nulos
c1.write(px.scatter_mapbox(hurtos , lat= 'latitud', lon= 'longitud', color= 'comuna',
                  color_continuous_scale = px.colors.cyclical.IceFire, size_max = 30, zoom = 10))
#neiva
c2.markdown("<h3 style='text-align: center; color: black;'>Victimas por comuna Neiva </h3>", unsafe_allow_html=True)

d2 = hn['comuna'].groupby(hm['hurtos']).value_counts()
d2 = d2.to_frame(name = 'cantidad_de_hurtos').reset_index()
df2 = d2.drop('hurtos',axis=1)

# Código para convertir el DataFrame en una tabla plotly resumen
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df2.columns),
    fill_color='lightgrey',
    line_color='darkslategray'),
    cells=dict(values=[df2.comuna, df2.cantidad_de_hurtos,],fill_color='white',line_color='lightgrey'))
   ])
fig.update_layout(width=500, height=450)


c2.write(fig)



# 3.¿Cuales son los bienes con mayor indice de hurto y que poblacion es la victima ?
st.markdown("<h3 style='text-align: center; color: black;'>Categoria de bienes hurtados</h3>", unsafe_allow_html=True)

listac = hm['categoria_bien'].value_counts().index[hm['categoria_bien'].value_counts()<60]
listac = listac.to_list() #Convertir a lista
number_of_elements = len(listac)
#Remplaxar lista en el dt
hm['categoria_bien'] = hm['categoria_bien'].replace(listac, "categoria especial")


fig = px.pie(hm, values = 'hurtos', names ='categoria_bien',
             title= '<b>Categorias Medellín<b>',
             color_discrete_sequence=px.colors.qualitative.G10)
fig.update_layout(
    xaxis_title = 'Numero de hurtos',
    yaxis_title = 'Tipo de bien',
    template = 'simple_white',
    title_x = 0.5)
st.write(fig)
# neiva 3. ¿Cuales es el rango de hora mas comun en la cuál la poblacion es más susceptible a ser victima de hurto y las caracteristicas de la poblacion (sexo) ?
st.markdown("<h3 style='text-align: center; color: black;'>Cantidad de hurtos por rangos de hora Neiva</h3>", unsafe_allow_html=True)

fig = px.sunburst(hn, path=['rango-hora', 'sexo'], values='hurtos',color_discrete_sequence=px.colors.sequential.RdBu)
st.write(fig)




# 4. ¿Cuales son los barrios con mayor indice de hurto ?
#medellin
c1.markdown("<h3 style='text-align: center; color: black;'>Índice de robos en barrios de Medellín</h3>", unsafe_allow_html=True)

d2 = hm['nombre_barrio'].groupby(hm['hurtos']).value_counts()
d2 = d2.to_frame(name = 'cantidad_de_hurtos').reset_index()
df2 = d2.drop('hurtos',axis=1)

# Código para convertir el DataFrame en una tabla plotly resumen
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df2.columns),
    fill_color='lightgrey',
    line_color='darkslategray'),
    cells=dict(values=[df2.nombre_barrio, df2.cantidad_de_hurtos,],fill_color='white',line_color='lightgrey'))
   ])
fig.update_layout(width=500, height=450)
c1.write(fig)
#neiva
c2.markdown("<h3 style='text-align: center; color: black;'>Índice de robos en barrios de Neiva</h3>", unsafe_allow_html=True)

d2 = hn['nombre_barrio'].groupby(hm['hurtos']).value_counts()
d2 = d2.to_frame(name = 'cantidad_de_hurtos').reset_index()
df2 = d2.drop('hurtos',axis=1)

# Código para convertir el DataFrame en una tabla plotly resumen
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df2.columns),
    fill_color='lightgrey',
    line_color='darkslategray'),
    cells=dict(values=[df2.nombre_barrio, df2.cantidad_de_hurtos,],fill_color='white',line_color='lightgrey'))
   ])
fig.update_layout(width=500, height=450)
c2.write(fig)



# 5. ¿Cuales es la modalidad de hurto mas comun ? ¿ Y cual es el sexo de la victima?
#medellin
c1.markdown("<h3 style='text-align: center; color: black;'>Tipo de modalidad usada y el Sexo victimas de hurto Medellín</h3>", unsafe_allow_html=True)

g1 = hm.groupby(['sexo','modalidad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="modalidad", y="hurtos", color="sexo", title="Modalidades Medellín", barmode = 'group')
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c1.write(fig)
#neiva
c2.markdown("<h3 style='text-align: center; color: black;'>Tipo de modalidad usada y el Sexo victimas de hurto Neiva</h3>", unsafe_allow_html=True)

g1 = hn.groupby(['sexo','modalidad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="modalidad", y="hurtos", color="sexo", title="Modalidades Neiva", barmode = 'group')
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c2.write(fig)


# 6.¿Cuales es el arma mas empleada para realizar hurtos?
#medellin
# crear gráfica
fig = px.pie(hm, values = 'hurtos', names ='arma_medio',
             title= '<b>Hurtos por tipo de arma en la ciudad de Medellín<b>',hole = .3,
             color_discrete_sequence=px.colors.qualitative.G10)
# poner detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5,)
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c1.write(fig)
#neiva
fig = px.pie(hn, values = 'hurtos', names ='arma_medio',
             title= '<b>Hurtos por tipo de arma en la ciudad de Neiva<b>',hole = .3,
             color_discrete_sequence=px.colors.qualitative.G10)
# poner detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5,)
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c2.write(fig)


# 7. ¿Cuales es el estado civil y el genero mas hurtado? medellin
st.markdown("<h3 style='text-align: center; color: black;'>Estado civil y el género más hurtado</h3>", unsafe_allow_html=True)

g1 = hm.groupby(['sexo','estado_civil'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="estado_civil", y="hurtos", color="sexo", title="Estado civil y el Sexo de las victimas de hurto en Medellín", barmode = 'group')
st.write(fig)

    
#8. ¿Cuales es el tipo de lugar que mas presenta hurtos?   
#medellin
# Código para generar el DataFrame
c1.markdown("<h3 style='text-align: center; color: black;'>Cantidad de hurtos por lugares Medellín</h3>", unsafe_allow_html=True)

d2 = hm['lugar'].groupby(hm['hurtos']).value_counts()
d2 = d2.to_frame(name = 'cantidad_de_hurtos').reset_index()
df2 = d2.drop('hurtos',axis=1)

# Código para convertir el DataFrame en una tabla plotly resumen
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df2.columns),
    fill_color='lightgrey',
    line_color='darkslategray'),
    cells=dict(values=[df2.lugar, df2.cantidad_de_hurtos,],fill_color='white',line_color='lightgrey'))
   ])
fig.update_layout(width=500, height=450)
c1.write(fig)
#neiva.
c2.markdown("<h3 style='text-align: center; color: black;'>Cantidad de hurtos por lugares Neiva</h3>", unsafe_allow_html=True)

d2 = hn['lugar'].groupby(hm['hurtos']).value_counts()
d2 = d2.to_frame(name = 'cantidad_de_hurtos').reset_index()
df2 = d2.drop('hurtos',axis=1)

# Código para convertir el DataFrame en una tabla plotly resumen
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df2.columns),
    fill_color='lightgrey',
    line_color='darkslategray'),
    cells=dict(values=[df2.lugar, df2.cantidad_de_hurtos,],fill_color='white',line_color='lightgrey'))
   ])
fig.update_layout(width=500, height=450)
c2.write(fig)




#9. ¿Cual es el año que presenta mas hurtos?
#medellín
st.markdown("<h3 style='text-align: center; color: black;'>Hurtos por cada año</h3>", unsafe_allow_html=True)

g1 = hm.groupby(['year'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="year", y="hurtos",labels={
                     "year": "Año",
                     "hurtos": "Hurtos",
                 },
                 title="Comportamiento hurtos por cada año en la ciudad de Medellín", barmode = 'group')
st.write(fig)



#10.¿Cual es el mes que presenta mas hurtos?
#Medellin
c1.markdown("<h3 style='text-align: center; color: black;'>Comportamiento de hurtos por mes Medellín</h3>", unsafe_allow_html=True)

g1 = hm.groupby(['month','year'])[['hurtos']].count().reset_index()

fig = px.bar(g1, x="month", y="hurtos",animation_frame='year',range_y=[0,550],title="Numero de hurtos por mes en Medellín", barmode = 'group')
c1.write(fig)
#neiva
c2.markdown("<h3 style='text-align: center; color: black;'>Comportamiento de hurtos por mes Neiva</h3>", unsafe_allow_html=True)

g1 = hn.groupby(['mes','año'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="mes", y="hurtos", color= "año",title="Numero de hurtos por mes Neiva")
c2.write(fig)
#neiva 10. ¿Cual es sexo y el transporte de la poblacion mas hurtada?


#11. ¿Cual es el dia de la semana que presenta mas hurtos y a que sexo hurtan mas?
#medellín
c1.markdown("<h3 style='text-align: center; color: black;'>Comportamiento de hurtos por día Medellín</h3>", unsafe_allow_html=True)

g1 = hm.groupby(['sexo','day'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="day", y="hurtos", color="sexo", title="Hurtos por día en Medellín", barmode = 'group')
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c1.write(fig)
#neiva
c2.markdown("<h3 style='text-align: center; color: black;'>Comportamiento de hurtos por día en Neiva</h3>", unsafe_allow_html=True)

g1 = hn.groupby(['sexo','day'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="day", y="hurtos", color="sexo", title="Hurtos por día en Neiva", barmode = 'group')
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c2.write(fig)



# 12. ¿Cual es sexo y la edad de la poblacion mas hurtada?
g1 = hm.groupby(['sexo','rango_edad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="rango_edad", y="hurtos", color="sexo", title="Sexo y rango edad con mas hurtos en la ciudad de Medellín", barmode = 'group')
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c1.write(fig)

#neiva
g1 = hn.groupby(['sexo','rango_edad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="rango_edad", y="hurtos", color="sexo", title="Sexo y rango edad con mas hurtos en la ciudad de Neiva", barmode = 'group')
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
)
c2.write(fig)


#neiva 12.¿Cual es el transporte mas comun usado por el agresor?
st.markdown("<h3 style='text-align: center; color: black;'>Medio de transporte del agresor Neiva</h3>", unsafe_allow_html=True)
fig = px.sunburst(hn, path=['móvil_agresor', 'sexo'], values='hurtos',color_discrete_sequence=px.colors.sequential.RdBu)
st.write(fig)



#########################UNION####################
st.markdown("<h1 style='text-align: center; color: #3C9AD0;'> Bases unidas </h1>", unsafe_allow_html=True)

#1.¿Cuales son las caracteristicas mas comunes de la poblacion victima de hurtos (Rango de edad y sexo) ?
st.markdown("<h3 style='text-align: center; color: black;'>Sexo y edad de las victimas </h3>", unsafe_allow_html=True)

g1 = dfunion.groupby(['sexo','rango_edad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="rango_edad", y="hurtos", color="sexo", title="Rango de edades y Sexo de las victimas de hurto ", barmode = 'group')
fig.update_layout(xaxis_title="<b>Rango de edad<b>",
                  yaxis_title="<b>Edades<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')
st.write(fig)

#2. ¿Cuales es la cuidad con mas robos y el sexo de las victimas ?
st.markdown("<h3 style='text-align: center; color: black;'>Cantidad de robos por ciudad y sexo </h3>", unsafe_allow_html=True)

g1 = dfunion.groupby(['ciudad','sexo'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="sexo", y="hurtos", color="ciudad", title="Rango de edades y Sexo de las victimas de hurto ", barmode='overlay')
fig.update_layout(xaxis_title="<b>Sexo<b>",
                  yaxis_title="<b>Hurtos<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')
st.write(fig)

#3.¿Cual es la modalidad mas empleada para robar 
st.markdown("<h3 style='text-align: center; color: black;'>Modalidad de hurtos</h3>", unsafe_allow_html=True)

g1 = dfunion.groupby(['modalidad','ciudad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="modalidad", y="hurtos", color="ciudad", title="Modalidad empleada  y Sexo de las victimas de hurto ")
fig.update_layout(xaxis_title="<b>Modalidad usada<b>",
                  yaxis_title="<b>Hurtos<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')
st.write(fig)

#4.¿Cual es el mes con mas hurtos y en a que sexo?
st.markdown("<h3 style='text-align: center; color: black;'>Hurtos por mes y sexo</h3>", unsafe_allow_html=True)

g1 = dfunion.groupby(['sexo','mes'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="mes", y="hurtos", color="sexo", title="Mes y sexo con mas hurtos", barmode='group')
fig.update_layout(xaxis_title="<b>Mes<b>",
                  yaxis_title="<b>Hurtos<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')
st.write(fig)

#5. ¿Cual es el arma mas empleada?
st.markdown("<h3 style='text-align: center; color: black;'>Armas empleadas</h3>", unsafe_allow_html=True)
fig = px.pie(dfunion, values = 'hurtos', names ='arma_medio',
             title= 'Porcentaje de uso de armas',
             color_discrete_sequence=px.colors.qualitative.G10)
fig.update_layout(
    xaxis_title = 'Numero de hurtos',
    yaxis_title = 'Arma empleada',
    template = 'simple_white',
    title_x = 0.1)
st.write(fig)

#6.¿Sexo con mayor probabilidad de ser hurtado?
st.markdown("<h3 style='text-align: center; color: black;'>Probabilidad de ser asaltado debido al género</h3>", unsafe_allow_html=True)

fig = px.pie(dfunion, values = 'hurtos', names ='sexo',
             title= '<b>Género con mayor probabilidad de ser asaltado<b>',
             color_discrete_sequence=px.colors.qualitative.G10)
fig.update_layout(
    xaxis_title = 'Numero de hurtos',
    yaxis_title = 'Sexo',
    template = 'simple_white',
    title_x = 0.1)
st.write(fig)

#7.¿Dia de la semana y ciudad con mas hurtos?
st.markdown("<h3 style='text-align: center; color: black;'>Hurtos por día y sexo</h3>", unsafe_allow_html=True)
g1 = dfunion.groupby(['sexo','dia'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="dia", y="hurtos", color="sexo", title="Genero y dia de la semana mas hurtados ")
st.write(fig)

#8. ¿Lugar y ciudad con mas hurtos?
df2 = dfunion.groupby(['ciudad','lugar'],)[['hurtos']].count().sort_values(by="hurtos",ascending= False) 
df2

#9. Medio de transporte con mas probabilidades de sufrir un robo y la ciudad?
st.markdown("<h3 style='text-align: center; color: black;'>Probabilidad de ser robado en cierto medio de transporte</h3>", unsafe_allow_html=True)
g1 = dfunion.groupby(['ciudad','medio_transporte'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="medio_transporte", y="hurtos", color="ciudad", title="Medio de transporte mas hurtado por ciudad ")
st.write(fig)

#10.  ¿Edad con mas hurtos en cada ciudad?
st.markdown("<h3 style='text-align: center; color: black;'>Hurtos por edad</h3>", unsafe_allow_html=True)

g1 = dfunion.groupby(['edad','ciudad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="edad", y="hurtos", color="ciudad", title="Genero y dia de la semana mas hurtados ")
st.write(fig)

#11. ¿Cual es la modalidad mas empleada y a que sexo es aplicada?
st.markdown("<h3 style='text-align: center; color: black;'>Modalidad de hurto y sexo</h3>", unsafe_allow_html=True)

g1 = dfunion.groupby(['sexo','modalidad'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="modalidad", y="hurtos", color="sexo", title="Genero de la victima y metodo que es empleado ", barmode='group')
st.write(fig)

#12. ¿Cual es el arma mas empleada para atracar a que tipo de victima(sexo)?
st.markdown("<h3 style='text-align: center; color: black;'>Arma usada y sexo</h3>", unsafe_allow_html=True)

g1 = dfunion.groupby(['sexo','arma_medio'])[['hurtos']].count().reset_index()
fig = px.bar(g1, x="arma_medio", y="hurtos", color="sexo", title="Arma empleada y sexo de la victima ", barmode='group')
st.write(fig)
