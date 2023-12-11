import dash
from dash import dcc, html 
from dash.dependencies import Input, Output  # Importar Input y Output para el callback
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('carpetasFGJ_2023.csv')  # Asegúrate de que el nombre del archivo sea correcto

# Filtrar para asegurar que todas las filas tengan coordenadas
df = df.dropna(subset=['latitud', 'longitud'])

# Obtener la lista de tipos de crimen únicos
tipos_de_crimen = df['delito'].unique()

# Crear la figura del mapa de calor inicial
fig = px.density_mapbox(df, lat='latitud', lon='longitud', 
                        radius=10, 
                        center={"lat": 19.36, "lon": -99.133209},  # Centro en la Ciudad de México
                        zoom=10, 
                        mapbox_style="mapbox://styles/mapbox/light-v10")  # Puedes cambiar el estilo del mapa aquí

fig.update_layout(mapbox_accesstoken='pk.eyJ1IjoibHVpczMyNyIsImEiOiJjbHBtcXhwYmwwYWxiMnZxNGthZWNqaXJtIn0.PF9l_lle13ipWP6hf3q-qQ')

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Mapa de Calor de Criminalidad en la Ciudad de México", className='h1'),

    # Agregar un Dropdown para seleccionar el tipo de crimen
    dcc.Dropdown(
        id='dropdown-delito',
        options=[{'label': tipo, 'value': tipo} for tipo in tipos_de_crimen],
        value=None,  # Sin selección inicial
        multi=True,  # Permite selección múltiple
        style={'width': '95%'}  # Establecer el ancho del Dropdown
    ),


    dcc.Graph(id='mapa-de-calor', className='graph')
], className='body')

# Definir el callback para actualizar el mapa de calor según el tipo de crimen seleccionado
@app.callback(
    Output('mapa-de-calor', 'figure'),
    [Input('dropdown-delito', 'value')]
)
def actualizar_mapa_de_calor(tipos_seleccionados):
    # Verificar si no se ha seleccionado ningún tipo de crimen
    if not tipos_seleccionados:
        # Mostrar un mensaje o texto predeterminado en lugar del mapa
        return {'data': [], 'layout': {'title': 'Selecciona un tipo de delito'}}

    # Filtrar el DataFrame según los tipos de crimen seleccionados
    df_filtrado = df[df['delito'].isin(tipos_seleccionados)]

    # Crear una nueva figura del mapa de calor con los datos filtrados
    fig_actualizado = px.density_mapbox(df_filtrado, lat='latitud', lon='longitud', 
                                        radius=10, 
                                        center={"lat": 19.36, "lon": -99.133209},  
                                        zoom=10, 
                                        mapbox_style="mapbox://styles/mapbox/light-v10")  

    fig_actualizado.update_layout(mapbox_accesstoken='pk.eyJ1IjoibHVpczMyNyIsImEiOiJjbHBtcXhwYmwwYWxiMnZxNGthZWNqaXJtIn0.PF9l_lle13ipWP6hf3q-qQ')

    return fig_actualizado

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=False)