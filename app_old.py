import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly
from plotly import graph_objs as go
from plotly.graph_objs import *
from wordcloud import WordCloud, STOPWORDS
from flask import Flask
import pandas as pd
import numpy as np
import os
import copy


app = dash.Dash(__name__)
server = app.server


mapbox_access_token = "pk.eyJ1IjoiZ2lubnlxZyIsImEiOiJjam9zcnlsemwwZHZrM3JvOTZudm5uY2E3In0.LhMpmoHGbUjWc6wmypE9cg" #fill this field with your Mapbox key

raw = pd.read_csv('https://raw.githubusercontent.com/ginnyqg/dashboard/master/acquisitions.csv')



# Boostrap CSS.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

layout = dict(
    # autosize=True,
    # height=800,
    font=dict(color="#191A1A", family='Arial, sans-serif'),
    titlefont=dict(color="#191A1A", size='12', family='Arial, sans-serif'),
    margin=dict(
        l=5,
        r=5,
        b=5,
        t=5
    ),
    hovermode="closest",
    legend=dict(font=dict(size=10), orientation='h'),
    # title='<b>Acquisition by Top 7 Tech Companies</b>',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
    )
)


# Creating layouts for datatable
layout_right = copy.deepcopy(layout)
layout_right['height'] = 200
# layout_right['margin-top'] = '10'
layout_right['font-size'] = '12'


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
            "title": '<b>Geo View of Acquired Companies by Parent Company</b>',
            "width": 550,
            "height": 350,
            "margin": {
            "l": 0,
            "r": 0,
            "b": 20,
            "t": 30},
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
                    'Company Acquisitions by 7 Tech Giants',
                    style={"font-family": "Arial, sans-serif",
                           "font-weight": "bold",
                           'margin-top': '5',
                           "margin-bottom": "0"},
                    className='ten columns',
                ),
                dcc.Link('Code', href='https://github.com/ginnyqg/dashboard', 
                    style = {'float': 'right',
                             'margin-top': '5'}),
                html.P('\u00A0\u00A0\u00A0', 
                    style = {'float': 'right',
                             'margin-top': '5'}),
                dcc.Link('Data', href='https://www.kaggle.com/shivamb/company-acquisitions-7-top-companies', 
                    style = {'float': 'right',
                            'margin-top': '5'}),
                html.H4(
                    'between 1987 and 2018',
                    style={'font-family': 'Arial, sans-serif',
                           "font-size": "120%",
                           "width": "80%",
                           "float": "left"
                           },
                    className='ten columns',
                ),
            ],
            className='row'
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        # html.P('Geo View of Acquired Companies by Parent Companies',
                        #         style={'font-family': 'Arial, sans-serif',
                        #                'font-weight': 'bold'}),
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
                    className='twelve columns',
                    style={
                    # 'margin-top': '10',
                           'margin-bottom': '10'}
                ),
            ],
            className='row'
        ),

        # Map, barchart, donut chart, word cloud, text, table
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True, 
                                  style={'margin-top': '0'}
                                  )
                    ], className = "seven columns"
                ),

                html.Div(
                    [
                        dcc.Graph(id="bar-chart"
                            )
                    ], className="five columns")
                ],
                className="row"
                ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='donut-chart',
                                  animate=True, 
                                  style={'margin-top': '0'}
                                  )
                    ], className = "six columns"
                ),

                html.Div(
                    [
                        dcc.Graph(id="word-cloud"
                            )
                    ], className="six columns")
                ],
                className="row"
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
                style=layout_right,
                className="twelve columns"
                )
    ]
    , 
    className='ten columns offset-by-one')




# Callbacks and functions for datatable
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



# Callbacks and functions for bar-chart
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
        # autosize = False,
        width = 400,
        height = 280,
        margin = dict(
        l = 50,
        r = 50,
        b = 50,
        t = 50),
        title = '<b>Number of Acquisitions by Parent Company</b>',
        font=dict(color = "#191A1A", 
                  family = 'Arial, sans-serif'),
    #     xaxis = go.layout.XAxis(
    #     title = 'Top 7 Tech Companies'
    #     ),
        yaxis = go.layout.YAxis(
        title = 'Count'
        )
        )

    return go.Figure(data = data, layout = layout)



# Callbacks and functions for donut-chart
@app.callback(
    Output('donut-chart', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    amt_PC = pd.DataFrame(dff.groupby(['ParentCompany'])['Value (USD)'].sum())
    amt_PC = amt_PC.sort_values(by = 'Value (USD)', ascending = True)

    return {
      "data": [
        {
          "values": round(amt_PC['Value (USD)']/1000000000, 2),
          "labels": amt_PC.index,
          "domain": {"x": [0, 1]},
          "hoverinfo": "label + value",
          "hole": .4,
          "type": "pie"
        }],
        
      "layout": {
            "title":"<b>Value of Acquisition by Parent Company(US$B)</b>",
            "font": {"color": "#191A1A", 
                     "family": "Arial, sans-serif"},
            "align": 'center',
            "width": 500,
            "height": 300,
            "margin": {
            "l": 20,
            "r": 20,
            "b": 20,
            "t": 30},
            "showlegend": False,
            "annotations": [
                {
                    "font": {
                    "size": 14
                    },
                    "showarrow": False,
                    "text": "Parent <br>Company</br>",
                    "x": 0.5,
                    "y": 0.5
                }
            ]
        }
    }



# Callbacks and functions for word-cloud
@app.callback(
    Output('word-cloud', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    text = dff.Business
    wc = WordCloud(stopwords = set(STOPWORDS),
                   max_words = 200,
                   max_font_size = 100)
    wc.generate(str(text))
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list
    

    trace = go.Scatter(
                    x=x, 
                    y=y, 
                    textfont = dict(size=new_freq_list,
                                    color=color_list),
                    hoverinfo='text',
                    hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                    mode="text",  
                    text=word_list
                    )
    
    layout = go.Layout(
                   xaxis=dict(showgrid=False, 
                              showticklabels=False,
                              zeroline=False,
                              automargin=True),
                   yaxis=dict(showgrid=False,
                              showticklabels=False,
                              zeroline=False,
                              automargin=True),
#                        autosize = True,
                   title = '<b>Type of Businesses Acquired</b>',
                   font=dict(color="#191A1A", family='Arial, sans-serif'),
                   width = 500,
                   height = 300,
                   margin = dict(
                    l = 20,
                    r = 20,
                    b = 30,
                    t = 30)
                          )

    return go.Figure(data=[trace], layout=layout)



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





