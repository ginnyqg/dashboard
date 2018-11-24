import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
import pandas as pd
import numpy as np
import os
import copy


app = dash.Dash(__name__)
server = app.server


mapbox_access_token = "pk.eyJ1IjoiZ2lubnlxZyIsImEiOiJjam9zcnlsemwwZHZrM3JvOTZudm5uY2E3In0.LhMpmoHGbUjWc6wmypE9cg" #fill this field with your Mapbox key
raw = pd.read_csv('/Users/qinqingao/Desktop/Columbia/Courses/Fall 2018/APAN 5500 Viz/HW/A4/acquisitions.csv')



# Boostrap CSS.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

layout = dict(
    # autosize=True,
    # height=800,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=5,
        r=5,
        b=5,
        t=5
    ),
    hovermode="closest",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Acquisition by Top 7 Tech Companies',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
    )
)


# Controls (dropdowns)
group = ['All']
group = group + ['Low', 'Medium', 'High', 'Very High']
group_class = [{'label': str(item),
                'value': str(item)}
                for item in group]



# Creating layouts for datatable
layout_right = copy.deepcopy(layout)
layout_right['height'] = 300
# layout_right['margin-top'] = '10'
layout_right['font-size'] = '12'

mp_max = raw['Value (USD)'].max()
mp_min = raw['Value (USD)'].min()


# Components style
def color_scale(md, selected_row_indices=[]):
    color = []
    max_score = mp_max
    min_score = mp_min
    for row in md['Value (USD)']:
        scale = (row - mp_min)/(mp_max - mp_min)
        if scale <= 0.06:
            color.append("#26EC04")
        elif scale <= 0.12:
            color.append("#8FDB44")
        elif scale <= 0.18:
            color.append("#A5D643")
        elif scale <= 0.24:
            color.append("#B8D343")
        elif scale <= 0.30:
            color.append("#B8D343")
        elif scale <= 0.36:
            color.append("#DBCD44")
        elif scale <= 0.42:
            color.append("#E1CD44")
        elif scale <= 0.48:
            color.append("#F0CB45")
        elif scale <= 0.54:
            color.append("#F3C644")
        elif scale <= 0.60:
            color.append("#F2BE41")
        elif scale <= 0.66:
            color.append("#F0AE3D")
        elif scale <= 0.72:
            color.append("#EFA73B")
        elif scale <= 0.78:
            color.append("#EE9F39")
        elif scale <= 0.84:
            color.append("#ED8934")
        elif scale <= 0.90:
            color.append("#E95729")
        else:
            color.append("#FD0101")
    for i in selected_row_indices:
        color[i] = '#1500FA'
    return color


def gen_map(raw):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    csl = [[0, 'rgb(255, 255, 255)'], [0.0005, 'rgb(255, 243, 234)'], [0.001, 'rgb(255, 230, 208)'], [0.01, 'rgb(255, 175, 106)'], [0.05, 'rgb(255, 161, 81)'], [0.25, 'rgb(255, 134, 30)'], [1, 'rgb(255, 118, 0)']]

    return {
        "data": [{
        "type": 'choropleth',
        "locations": raw['Country'],
        "z": raw['Value (USD)'],
#         text = raw['Country'],
        "colorscale": csl,
        # colorscale = 'Rainbow',
        "autocolorscale": False,
        "showscale": False,
        "marker": {
        "line": {
        "color": 'rgb(180,180,180)',
        "width": 1
            }},
#         tick0 = 0,
        "zmin": 0,
#         dtick = 1000,
        # colorbar = dict(
        #     title = 'US$ B'
        # )
        }
            ],
        "layout": {
    # "title": '<b>Worldwide Acquisition Value</b>',
    "width": 600,
    "height": 350,
    "margin": {
    "l": 0,
    "r": 0,
    "b": 0,
    "t": 0},
    "geo": {
        "showframe": False,
        "showcoastlines": True,
        "projection": {
        "type": 'equirectangular'
        }
    }
}
    }



# Layout
app.layout = html.Div([
    # Title - Row
    html.Div(
        [
            html.H2(
                'Acquisition by Top 7 Tech Companies',
                style={'font-family': 'Helvetica',
                       "margin-top": "15",
                       "margin-bottom": "0"},
                className='Eight columns',
            ),
            # html.Img(
            #     src="http://static1.squarespace.com/static/546fb494e4b08c59a7102fbc/t/591e105a6a496334b96b8e47/1497495757314/.png",
            #     className='two columns',
            #     style={
            #         'height': '9%',
            #         'width': '9%',
            #         'float': 'right',
            #         'position': 'relative',
            #         'padding-top': 10,
            #         'padding-right': 0
            #     },
            # ),
            html.P(
                'Geo View for Acquired Companies',
                style={'font-family': 'Helvetica',
                       "font-size": "120%",
                       "width": "80%"},
                className='six columns',
            ),
        ],
        className='row'
    ),

    # Selectors
    html.Div(
        [
            html.Div(
                [
                    html.P('Choose Parent Companies:'),
                    dcc.Checklist(
                            id = 'PComp',
                            options=[
                                {'label': 'Google', 'value': 'Google'},
                                {'label': 'Microsoft', 'value': 'Microsoft'},
                                {'label': 'Facebook', 'value': 'Facebook'},
                                {'label': 'Apple', 'value': 'Apple'},
                                {'label': 'Twitter', 'value': 'Twitter'},
                                {'label': 'IBM', 'value': 'IBM'},
                                {'label': 'Yahoo', 'value': 'Yahoo'}
                            ],
                            values=['Google', 'Microsoft', 'Facebook', 'Apple', 'Twitter', 'IBM', 'Yahoo'],
                            labelStyle={'display': 'inline-block'}
                    ),
                ],
                className='six columns',
                style={'margin-top': '10'}
            ),
        ],
        className='row'
    ),

    # Map + table + Histogram
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='map-graph',
                              animate=True, 
                              style={'margin-top': '0'}
                              )
                ], className = "six columns"
            ),

            html.Div(
                [
                    dcc.Graph(id="bar-chart")],
                    className="six columns")
            ], className="row"
            ),

            html.Div(
                [
                    dt.DataTable(
                        rows=raw.to_dict('records'),
                        columns=raw.columns,
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        selected_row_indices=[],
                        id='datatable'),
                ],
                # style=layout_right,
                className="twelve columns"
            )], className='ten columns offset-by-one')




# Callbacks and functions
@app.callback(
    Output('datatable', 'rows'),
    [dash.dependencies.Input('PComp', 'values')
    ])
def update_selected_row_indices(PComp):
    map_aux = raw.copy()

    # PCompany filter
    map_aux = map_aux[map_aux['ParentCompany'].isin(PComp)]

    rows = map_aux.to_dict('records')
    return rows



@app.callback(
    Output('datatable', 'selected_row_indices'),
    [Input('bar-chart', 'selectedData')],
    [State('datatable', 'selected_row_indices')])

def update_selected_row_indices(selectedData, selected_row_indices):
    if selectedData:
        selected_row_indices = []
        for point in selectedData['points']:
            selected_row_indices.append(point['pointNumber'])
    return selected_row_indices




@app.callback(
    Output('bar-chart', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    cnt_PC = pd.DataFrame({'PComp': dff.ParentCompany.value_counts()})
    cnt_PC = cnt_PC.sort_values(by = 'PComp', ascending = False)


    data = Data([
         go.Bar(
                    x = cnt_PC.index,
                    y = cnt_PC.PComp,
    #                 text = cnt_PC.PComp,
    # #                 font = dict(
    # #                 color = "black",
    # #                 size = 12
    # #                 ),
    #                 textposition = 'outside',
                    marker = dict(
                            color = 'orange',
                            line = dict(
                            color = 'orange',
                            width = 1.5)
                            ),
                    opacity = 0.6
            )])

    layout = go.Layout(
        autosize = False,
        width = 550,
        height = 300,
        margin = dict(
        l = 120,
        r = 10,
        b = 50,
        t = 50),
        title = '<b>Number of Acquisitions</b>',
    #     xaxis = go.layout.XAxis(
    #     title = 'Top 7 Tech Companies'
    #     ),
        yaxis = go.layout.YAxis(
        title = 'Count'
        )
        )

    return go.Figure(data = data, layout = layout)



@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])

def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)



if __name__ == '__main__':
    app.run_server(debug=True)





