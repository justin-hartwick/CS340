# dashboard.py – SNHU CS-340 Dash App (Justin Hartwick)

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_leaflet as dl
import pandas as pd
from animal_shelter import AnimalShelter

# MongoDB Connection Setup
username = "aacuser"
password = "SNHU1234"
host = "127.0.0.1"
port = 27017
db_name = "aac"
collection_name = "animals"

# Create AnimalShelter instance
shelter = AnimalShelter(username, password, host, port, db_name, collection_name)

# Load data from MongoDB
df = pd.DataFrame.from_records(shelter.read({}))
if "_id" in df.columns:
    df.drop(columns=["_id"], inplace=True)

# Dash app layout
app = Dash(__name__)

app.layout = html.Div([
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard – Justin Hartwick'))),
    html.Hr(),

    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        sort_action='native',
        filter_action='native',
        row_selectable='single',
        selected_rows=[0],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
    ),

    html.Br(),
    html.Hr(),

    html.Div(id='map-id', className='col s12 m6')
])

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    if not selected_columns:
        return []
    return [{'if': {'column_id': col}, 'background_color': '#D2F3FF'} for col in selected_columns]

@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'derived_virtual_data'),
     Input('datatable-id', 'derived_virtual_selected_rows')]
)
def update_map(viewData, index):
    dff = pd.DataFrame.from_dict(viewData)
    row = index[0] if index else 0

    lat = dff.iloc[row].get("location_lat") or 30.75
    lon = dff.iloc[row].get("location_long") or -97.48
    breed = dff.iloc[row].get("breed", "Unknown")
    name = dff.iloc[row].get("name", "Unnamed")

    marker_msg = f"{name} ({breed})"
    if lat == 30.75 and lon == -97.48:
        marker_msg += " (location unknown)"

    return [
        dl.Map(style={'width': '1000px', 'height': '500px'},
               center=[lat, lon], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            dl.Marker(position=[lat, lon], children=[
                dl.Tooltip(breed),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(marker_msg)
                ])
            ])
        ])
    ]

# Run the app locally on port 8052
if __name__ == '__main__':
    app.run(debug=True)
