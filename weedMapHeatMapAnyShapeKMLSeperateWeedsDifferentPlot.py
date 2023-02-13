import numpy as np
import pandas as pd 
from pykml import parser
import pandas as pd
from datetime import datetime, timedelta
from operator import attrgetter



# Class for weed

class Weed:
    # Specific definitions for location and type of weed, individual to each weed
    def __init__(self, latitude, longitude, type, date):
        self.longitude = longitude
        self.latitude = latitude
        self.type = type
        self.date = date.strftime('%Y-%m-%d')
        self.dateNoDash = self.date.split('-')
        self.dateInt = int(self.dateNoDash[0] + self.dateNoDash[1] + self.dateNoDash[2])

def date_to_int(date):
    dateNoDash = date.split('-')
    dateInt = int(dateNoDash[0] + dateNoDash[1] + dateNoDash[2])
    return dateInt



# Class for field corner

weedList = [Weed(-34.182, 139.962, 'weed1', datetime(2022, 6, 24)), Weed(-34.1844, 139.9615, 'weed2', datetime(2022, 6, 24)), Weed(-34.183, 139.9615, 'weed1', datetime(2022, 6, 24)), Weed(-34.1846, 139.961, 'weed2', datetime(2022, 6, 24)),
Weed(-34.1821, 139.9621, 'weed1', datetime(2022, 6, 25)), Weed(-34.18441, 139.96151, 'weed2', datetime(2022, 6, 25)), Weed(-34.1831, 139.96151, 'weed1', datetime(2022, 6, 25)), Weed(-34.18461, 139.9611, 'weed2', datetime(2022, 6, 25)),
Weed(-34.1822, 139.9622, 'weed1', datetime(2022, 6, 26)), Weed(-34.18442, 139.96152, 'weed2', datetime(2022, 6, 26)), Weed(-34.1832, 139.96152, 'weed1', datetime(2022, 6, 26)), Weed(-34.18462, 139.9612, 'weed2', datetime(2022, 6, 26)),
Weed(-34.1823, 139.9623, 'weed1', datetime(2022, 6, 27)), Weed(-34.18443, 139.96153, 'weed2', datetime(2022, 6, 27)), Weed(-34.1833, 139.96153, 'weed1', datetime(2022, 6, 27)), Weed(-34.18463, 139.9613, 'weed2', datetime(2022, 6, 27)),
Weed(-34.1824, 139.9624, 'weed1', datetime(2022, 6, 28)), Weed(-34.18444, 139.96154, 'weed2', datetime(2022, 6, 28)), Weed(-34.1834, 139.96154, 'weed1', datetime(2022, 6, 28)), Weed(-34.18464, 139.9614, 'weed2', datetime(2022, 6, 28)),
Weed(-34.1825, 139.9625, 'weed1', datetime(2022, 6, 29)), Weed(-34.18445, 139.96155, 'weed2', datetime(2022, 6, 29)), Weed(-34.1835, 139.96155, 'weed1', datetime(2022, 6, 29)), Weed(-34.18465, 139.9615, 'weed2', datetime(2022, 6, 29))]

# Code to read in KML file and parse it as a KML Object

kmlFile = r'C:\Users\scoop\OneDrive\Email attachments\Documents\FLUX\FLUX Testing.kml'

root = parser.fromstring(open(kmlFile, 'rb').read())

# Split the coordinates string from XML object into a list of [('latitude, lonigtude, altitude')]

coordinatesString = str(root.Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates)

# Split this list into [(latitude, longitude, altitude)] (split into individual strings not one which contains all 3 values)

coordinatesSplitString = list(coordinatesString.split())
 
# Split these values into 2 seperate latitude and longitude lists, also convert strings into floats

cornerLongitudes = []
cornerLatitudes = []

for x in range(len(coordinatesSplitString)):
    tempList1 = list(coordinatesSplitString[x].split(','))
    cornerLongitudes.append(float(tempList1[0]))
    cornerLatitudes.append(float(tempList1[1]))


# Find centre of the field

longitudeMiddle = sum(cornerLongitudes)/len(cornerLongitudes)
latitudeMiddle = sum(cornerLatitudes)/len(cornerLatitudes)

# Create the map plotter:

dataFrame = pd.DataFrame([[p.latitude, p.longitude, p.type, p.date] for p in weedList], columns = ('Latitude', 'Longitude', 'Type', 'Date'))

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

token = 'pk.eyJ1IjoicmVpbGx5LWgiLCJhIjoiY2xkaTQ4ZDhrMHp5czN2bnV4c3YzdHkxNSJ9.GrHE1HjlBcXd86fV5NhHxQ'

fieldDF = pd.DataFrame([[cornerLatitudes[p], cornerLongitudes[p]] for p in range(len(cornerLongitudes))], columns = ('Latitude', 'Longitude'))

fig1 = px.density_mapbox(data_frame = dataFrame, lat = 'Latitude', lon = 'Longitude', color_continuous_scale="viridis")

fig2 = px.line_mapbox(data_frame = fieldDF, lat = 'Latitude', lon = 'Longitude', )

fig = go.Figure(fig1.data + fig2.data)

from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR, dbc_css])

server = app.server

@app.callback(
    Output('dataTable', 'data'),
    Input('Date Selector', 'value'),
    Input('Slider Toggle', 'value')
)

def update_table(date, sliderON):

    if sliderON == 'ON':
        df = pd.DataFrame()
        for i in range(len(dataFrame)):
            if ((date[0]) <= date_to_int((dataFrame['Date'][i])) <= (date[1])):
                df = pd.concat([df, (dataFrame.iloc[[i]])], sort = False)
        dash_table.DataTable(
            id = 'dataTable',
            data = df.to_dict('records'), 
            columns = [{"name": i, "id": i} for i in df.columns]
        )
    else:
        df = dataFrame

    return df.to_dict('records')

dff = update_table([(dataFrame['Date'].min()), (dataFrame['Date'].max())], 'OFF')

app.layout = html.Div(
    children = [

        html.H1(
            children = 'Weed Map Dashboard',
            style = {
                'textAlign': 'center'
                }
        ),

        dbc.Row(children = [
            dbc.Col(width = 1),
            
            dbc.Col(        
                    children = [
                        html.Label('Map Selector', style = {'font-size': '15'}),
                        dbc.RadioItems(
                            options = [
                                {"label": "Heat Map", "value": "Heat Map"},
                                {"label": "Scatter Plot", "value": "Scatter Plot"}
                            ],
                            value = 'Scatter Plot', 
                            id = 'map selector',
                        )
                ]
            )],
            style = {'height': '10vh'},
            align = 'start'
        ),

        dbc.Row(style = {'height': '2vh'}),

        dbc.Row(children = [
                dbc.Col(width = 1),

                dbc.Col(
                    dcc.Graph(
                        id = 'Weed Map',
                        figure = fig,
                        style = {
                            'height': '50vh'
                        }   
                    ),
                    width = 7
                ),
                        
                dbc.Col(
                    dash_table.DataTable(
                        id = 'dataTable',
                        data = dff, 
                        columns = [{"name": i, "id": i} for i in dataFrame.columns],
                        fill_width=False,
                        cell_selectable=False,
                        style_table= {
                            'height': '50vh',
                            'overflowY': 'scroll'
                        },
                        style_cell = {
                            'width': '25vh',
                            'height': '2vh'
                        },
                        style_header={ 'border': '1px solid grey' },
                        # page_size = 14
                    ),
                    className = 'dbc',
                    width = 3
                )],
                style = {'height': '55vh'},
                align = 'start'
            ),

        dbc.Row(
            [
                dbc.Col(width = 1),
                dbc.Col(
                    dbc.RadioItems(['ON', 'OFF'], value = 'OFF', id = 'Slider Toggle', inline = True), width = 1
                )
            ],
            style = {'height': '2vh'}
        ),

        dbc.Row(children = [   
            dbc.Col(width = 1),         
            dbc.Col(
                dcc.RangeSlider(
                    id='Date Selector',
                    min=min(weedList, key = attrgetter('dateInt')).dateInt,
                    max=max(weedList, key = attrgetter('dateInt')).dateInt,
                    value=[min(weedList, key = attrgetter('dateInt')).dateInt, max(weedList, key = attrgetter('dateInt')).dateInt],
                    marks={date_to_int(i): i for i in dataFrame['Date']},
                    step=None   
                ),
                width = 10,
            ),
            dbc.Col(width = 1)],
            style = {'height': '10vh'},
            align = 'end'
        )
    ],
    className = 'pad-row'
)


@app.callback(
    Output('Weed Map', 'figure'),
    Input('map selector', 'value'),
    Input('Date Selector', 'value'),
    Input('Slider Toggle', 'value')
)

def update_figure(type, date, sliderON):
    
    if sliderON == 'ON':
        df = pd.DataFrame()
        for i in range(len(dataFrame)):
            if ((date[0]) <= date_to_int((dataFrame['Date'][i])) <= (date[1])):
                df = pd.concat([df, (dataFrame.iloc[[i]])], sort = False)
    else:
        df = dataFrame

    if type == 'Scatter Plot':
        fig2 = px.scatter_mapbox(data_frame= df, lat = 'Latitude', lon = 'Longitude')

        fig1 = px.line_mapbox(data_frame = fieldDF, lat = 'Latitude', lon = 'Longitude')

        fig = go.Figure(fig1.data + fig2.data)

        fig.update_traces(marker=dict(color='white'), line= dict(color='red'))
    elif type == 'Heat Map':

        fig1 = px.density_mapbox(data_frame = df, lat = 'Latitude', lon = 'Longitude')

        fig2 = px.line_mapbox(data_frame = fieldDF, lat = 'Latitude', lon = 'Longitude')

        fig = go.Figure(fig1.data + fig2.data)

        fig.update_layout(coloraxis_showscale=False)

    fig.update_layout(mapbox_style = 'satellite', mapbox_accesstoken = token, autosize = True, margin = dict(l=0, r=0, t=0, b=0))

    fig.update_mapboxes(zoom = 15, center = dict(lat = latitudeMiddle, lon = longitudeMiddle))
    
    return fig

if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload = False)

