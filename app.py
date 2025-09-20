import os
import pandas as pd
import geopandas as gpd
import json
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Input, Output, State
from datetime import datetime, date, timedelta
from utils import *
from dashboard_data import *


# Address data (needs to update regularly)
address_data = "data/..."

# Last modified timestamp of data
data_timestamp = datetime.fromtimestamp(os.stat(address_data).st_mtime)

df = pd.read_csv(address_data)

# Address data from the last n days
default = dashboard_data(df, start_date = (datetime.today() - timedelta(days = 7)).date(), end_date = date.today())

# Plotly scatter map
fig = default.get_scatter_map()

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.FLATLY])

# App layout
app.layout = \
    [
        html.Div([html.H1(children = "San Francisco Address Data")], style={'textAlign': 'center'}),

        html.Div([html.H2(children = f"Day-to-Day Dashboard")], style={'textAlign': 'center'}),

        dbc.Row(
            [
                dbc.Col(
                    html.Div([dcc.DatePickerRange(
                    # defaults to 7 day breakdown
                    start_date = (datetime.today() - timedelta(days = 7)).date(),
                    end_date = date.today(),
                    min_date_allowed = date(2018, 10, 11),
                    max_date_allowed = date.today(),
                    initial_visible_month = date.today(),
                    updatemode =  "bothdates",
                    clearable = True,
                    number_of_months_shown = 3,
                    id='date_range')], style={'textAlign': 'left', 'marginLeft': '16em'}),
                    width=6,
                    style={"border": "0px solid", "padding": "10px", 'marginLeft': '1em'},
                ),
                dbc.Col(
                    html.Div(children = [f"{default.dim[0]} addresses were updated"], id = "total", style={'textAlign': 'left','marginLeft': '1em'}),
                    style={"border": "0px solid", "padding": "20px"}
                )
            ]
        ), 

        html.Div(
                [
                html.Div(
                    [dcc.Graph(figure = fig, id = "map", clear_on_unhover = True)]), 
                html.Div([dash_table.DataTable(data = default.get_display_df().to_dict("records"),
                                     page_size = 20,
                                     id = "breakdown_table")], style={'fontSize': 10})
                ], style={'display': 'flex'}
                ),

        html.Div([html.P(children = f"Data retrieved on: {data_timestamp}")], style={'textAlign': 'left',
                                                                                    'marginLeft': '1em'}),
    ]

@app.callback(
        Output('breakdown_table', 'data'),
        Output("map", "figure"),
        Output("total", "children"),
        Input("date_range", "start_date"),
        Input("date_range", "end_date"))
def update_data(start_date, end_date):
    start_date_time = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_time = datetime.strptime(end_date, "%Y-%m-%d")
    updated_data = dashboard_data(df, start_date_time, end_date_time)
    return updated_data.get_display_df().to_dict("records"), updated_data.get_scatter_map(), f"{updated_data.dim[0]} addresses were updated"

@app.callback(
        Output("breakdown_table", "style_data_conditional", allow_duplicate=True),
        Input("breakdown_table", "selected_cells"),
        prevent_initial_call = True)
def update_table_styling(selected_cells):
    """
    Update table styling when:
     * Rows clicked or selected
     * ...
    """
    row_highlighting = [
        {
            "if": {"row_index": i["row"]}, 
            "background_color": "#ffd9d7"
        } for i in selected_cells]
    return row_highlighting

@app.callback(
        Output("breakdown_table", "style_data_conditional"),
        Input("map", "clickData"),
        prevent_initial_call = True)
def highlight_clicked_data(clickData):
    row_highlighting = [
        {
            "if": {'filter_query': f"{{EAS SubID}} = {clickData['points'][-1]['customdata'][1]}"}, 
            "background_color": "#ffd9d7"
        } ]
    print(row_highlighting)
    return row_highlighting

if __name__ == "__main__":
    app.run(debug = True)