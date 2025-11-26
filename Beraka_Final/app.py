import dash
from dash import html, dcc, Input, Output, State, dash_table
import pandas as pd
import os

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Archivos
RODEO = "inventario_rodeo.csv"
SOCIEDAD = "inventario_sociedad.csv"

# Crear si no existen
for archivo in [RODEO, SOCIEDAD]:
    if not os.path.exists(archivo):
        pd.DataFrame(columns=["Caravana","Categoría","Sexo","Raza","Peso_actual_kg",
                              "Fecha_nacimiento","Fecha_compra","Madre_caravana","Observaciones"]
                    ).to_csv(archivo, index=False)

def cargar(archivo):
    return pd.read_csv(archivo)

app.layout = html.Div([
    dcc.Location(id='url'),
    html.H1("Beraka Ganadería", style={'textAlign':'center','color':'#006400'}),
    dcc.Tabs(id="tabs", value='rodeo', children=[
        dcc.Tab(label='Mi Rodeo', value='rodeo'),
        dcc.Tab(label='Sociedad con el abuelo', value='sociedad'),
    ]),
    html.Div(id='contenido')
])

@app.callback(Output('contenido', 'children'),
              Input('tabs', 'value'))
def renderizar(tab):
    archivo = RODEO if tab == 'rodeo' else SOCIEDAD
    df = cargar(archivo)
    
    return html.Div([
        dash_table.DataTable(
            id='tabla',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            row_deletable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        ),
        html.Button("Borrar seleccionados y guardar", id="guardar", n_clicks=0),
        html.Div(id="dummy")
    ])

@app.callback(
    Output('dummy', 'children'),
    Input('guardar', 'n_clicks'),
    State('tabla', 'data'),
    State('tabs', 'value')
)
def guardar(n_clicks, rows, tab):
    if n_clicks > 0:
        archivo = RODEO if tab == 'rodeo' else SOCIEDAD
        pd.DataFrame(rows).to_csv(archivo, index=False)
    return ""

app.run_server(debug=False)