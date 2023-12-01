import dash
from dash import no_update
# import jupyter_dash
from dash import Dash, dash_table, dcc, callback, Output, Input, html, State
import dash_daq as daq

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

import plotly.express as px
import plotly.graph_objects as go

# import math

import pandas as pd

import numpy as np

import sqlite3, base64

from io import BytesIO 

from datetime import datetime
from datetime import timedelta
from datetime import date

# jupyter_dash.default_mode="external"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

server = app.server

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

############## extraer datos ################

df = pd.read_excel('https://github.com/eoyanedeli/ANID/raw/master/panel2/descargaTicket.xlsx', sheet_name = 'Hoja 1').loc[lambda x: (x['cuenta_que_recibe'] != 'latindex@anid.cl') & (x['cuenta_que_recibe'] != 'issn@anid.cl')]

cuentas = list(df.groupby('cuenta_que_recibe').size().reset_index(name = 'count')['cuenta_que_recibe'])

opciones = [{'label': f'{cuenta}', 'value': cuenta} for cuenta in cuentas]

# opciones.append({'label': 'General', 'value': 'general'})

app.layout = dbc.Container([
    
    ############ Título del dashboard ###############
    
    html.Div(className='row', children='Panel de control de tickets.',
             style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}),
    
    ########### Aquí van los gráficos ###############
    
    dbc.Row([
        
        ############ Gráfico de consultas por cuenta ##############
        
        dbc.Col(
            dcc.Graph(
                figure = px.pie(
                    df.groupby('cuenta_que_recibe').size().reset_index(name = 'número de consultas'),
                    names = 'cuenta_que_recibe',
                    values = 'número de consultas',
                    title = 'Número de consultas por cuenta'
                ),
                style = {'height': '400px', 'width': '600px'}
            ),
            width = 6
        ),
        
        ############ Gráfico de porcentaje por tipo de pregunta ################
        
        dbc.Col([
            dcc.Graph(id = 'graph-1'),
            dcc.Dropdown(
                id = 'select-1',
                options = opciones,
                value = None
            ),
            dcc.DatePickerRange(
                minimum_nights=5,
                clearable=True,
                with_portal=True,
                start_date = date(2023, 1, 1),
                end_date = date(2023, 11, 27),
                id = 'date-1'
            )],
            width = 6
        )
    ]),
    dbc.Row([
        
        ############ gráfico de respuestas por persona ################
        
        dbc.Col([
            dcc.Graph(id = 'graph-2'),
            dcc.Dropdown(
                id = 'select-2',
                options = opciones,
                value = None
            ),
            dcc.DatePickerRange(
                minimum_nights=5,
                clearable=True,
                with_portal=True,
                start_date = date(2023, 1, 1),
                end_date = date(2023, 11, 27),
                id = 'date-2'
            )],
            width = 6
        ),
        
        ############ Gráfico de consultas respondidas a tiempo #################
        
        dbc.Col([
            dcc.Graph(id = 'graph-3'),
            dcc.Dropdown(
                id = 'select-3',
                options = opciones,
                value = None
            ), 
            dcc.DatePickerRange(
                minimum_nights=5,
                clearable=True,
                with_portal=True,
                start_date = date(2023, 1, 1),
                end_date = date(2023, 11, 27),
                id = 'date-3'
            )],
            width = 6
        )
    ])
])

@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-3', 'figure')],
    [Input('select-1', 'value'),
     Input('select-2', 'value'),
     Input('select-3', 'value'),
     Input('date-1', 'start_date'),
     Input('date-1', 'end_date'),
     Input('date-2', 'start_date'),
     Input('date-2', 'end_date'),
     Input('date-3', 'start_date'),
     Input('date-3', 'end_date')]
)

def update_output(cuenta_1, cuenta_2, cuenta_3, start_date_1, end_date_1, start_date_2, end_date_2, start_date_3, end_date_3):
    
    df_solved = df.loc[lambda x: x['estado'] == 'Cerrado']
    # serie_actualizada = pd.to_datetime(df_solved['fecha_actualizacion'], errors = 'coerce')
    # serie_creada = pd.to_datetime(df_solved['fecha_creacion'], errors = 'coerce')
    # dt = df_solved.loc[lambda x: (start_date < pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d'))) &
    # (pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d')) < end_date)]

    if (start_date_1 != None) and  (end_date_1 != None):
        df_1 = df_solved.loc[lambda x: (start_date_1 < pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d'))) &
        (pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d')) < end_date_1)]
    else:
        df_1 = df_solved

    if (start_date_2 != None) and  (end_date_2 != None):
        df_2 = df_solved.loc[lambda x: (start_date_2 < pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d'))) &
        (pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d')) < end_date_2)]
    else:
        df_2 = df_solved
    
    if (start_date_3 != None) and  (end_date_3 != None):
        dt = df_solved.loc[lambda x: (start_date_3 < pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d'))) &
        (pd.to_datetime(pd.to_datetime(x['fecha_creacion'], errors = 'coerce').dt.strftime('%Y-%m-%d')) < end_date_3)]
    else:
        dt = df_solved
    
    # df_solved = df_solved.assign(in_time=(serie_actualizada - serie_creada).dt.days < 5)
    
    if cuenta_1 == None:
        df_clas = df_1.groupby('clasificación_pregunta').size().reset_index(name = 'número')
    else:
        df_clas = df_1.loc[lambda x: x['cuenta_que_recibe'] == cuenta_1].groupby('clasificación_pregunta').size().reset_index(name = 'número')
    
    if cuenta_2 == None:
        df_quien_contesto = df_2.groupby('quien_respondio').size().reset_index(name = 'Numero de respuestas')
    else:
        df_quien_contesto = df_2.loc[lambda x: x['cuenta_que_recibe'] == cuenta_2].groupby('quien_respondio').size().reset_index(name = 'Numero de respuestas')
    if cuenta_3 == None:
        df_a_tiempo = dt.groupby('Cumplimiento SLA').size().reset_index(name = 'Número')
    else:
        df_a_tiempo = dt.loc[lambda x: x['cuenta_que_recibe'] == cuenta_3].groupby('Cumplimiento SLA').size().reset_index(name = 'Número')
    
    # df_1 = df.groupby('clasificación_pregunta').size().reset_index(name = 'número')
    # df_quien_contesto = df_solved.groupby('quien_respondio').size().reset_index(name = 'Numero de respuestas')
    # df_a_tiempo = df_solved.groupby('in_time').size().reset_index(name = 'Número')
    
    fig_1 = px.pie(
                    df_clas,
                    values = 'número',
                    names = 'clasificación_pregunta',
                    title = 'Distribución de preguntas por clasificación'
                )
    fig_2 = px.bar(
                    df_quien_contesto,
                    x = 'quien_respondio',
                    y = 'Numero de respuestas',
                    title = 'Número de respuestas por persona'
                )
    fig_3 = px.pie(
                    df_a_tiempo,
                    values = 'Número',
                    names = 'Cumplimiento SLA',
                    title = 'Cumplimiento SLA',
                    category_orders={'Cumplimiento SLA': ['Cumple', 'No cumple']}
                )
    return fig_1, fig_2, fig_3

if __name__ == '__main__':
    app.run_server(debug=True)
# with open('index.html', 'w') as file:
#     file.write(app.to_html(full_html = False))