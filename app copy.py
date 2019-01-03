import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly
from plotly import graph_objs as go
from plotly.graph_objs import *
import matplotlib
from wordcloud import WordCloud, STOPWORDS
from flask import Flask
import pandas as pd
import numpy as np
import os
import copy
import urllib.parse

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from unidecode import unidecode


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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


conn = sqlite3.connect('twitter.db')
c = conn.cursor()


# def create_table():
#     c.execute("CREATE TABLE IF NOT EXISTS CAtweets(unix REAL, tweet TEXT)")
#     conn.commit()
# create_table()


# ckey = 'tTVzDuIq4E8eeyzTOiyGl13ot'
# csecret = 'QSBDZyzYHcZvxsyJG4sREX2TekCcvwTHmdTLPmdlofLnrVMORL'
# atoken = '351859770-mhjmvAs4l3s027lUuGVxt6bewqjiRDYgS8To9AIx'
# asecret = 'tZdYT9WUhz6sinVdTJZ8hUmgOQKRAunnIiR4NRSZxYxj4'

# class listener(StreamListener):

#     def on_data(self, data):
#         try:
#             data = json.loads(data)
#             tweet = unidecode(data['text'])
#             time_ms = data['timestamp_ms']
#             # print(time_ms, tweet)
#             c.execute("INSERT INTO CAtweets (unix, tweet) VALUES (?, ?)", (time_ms, tweet))
#             conn.commit()

#         except KeyError as e:
#             # print(str(e))
#             pass

#         return True


#     def on_error(self, status):
#         # print(status)
#         pass


# auth = OAuthHandler(ckey, csecret)
# auth.set_access_token(atoken, asecret)
# twitterStream = Stream(auth, listener())
# twitterStream.filter(track = ['#techacquisition', '#tech', '#technology', '#merger'])



df = pd.read_sql("SELECT * FROM CAtweets ORDER BY unix DESC LIMIT 7", conn)
df['date'] = pd.to_datetime(df['unix'], unit='ms')
df = df.drop(['unix'], axis=1)
df = df[['date','tweet']]


app.layout = html.Div([

    dcc.Tabs(id="tabs", colors={"border": "#e8e8e8", "primary": "gold", "background": "#F8FAE1"}, style={'font-family': 'Georgia', 'font-size': '120%'},
        children=[

        dcc.Tab(label='Introduction', 
            children=[
            html.Div(
            [
            html.H6("Gammadelt is a small startup that has found its niche in the fast growing and rapidly evolving tech industry by specializing in mobile apps. \
            	To plan for its future and better position itself in the tech industry, Gammadelt is looking into how the 7 tech giants -- Google, Microsoft, IBM, Apple, \
                Facebook, Twitter, and Yahoo -- have been acquiring companies over the years between 1987 and 2018.",
            style = {'font-family': 'Georgia', 'margin-top': '30', 'margin-bottom': '30'},
            className='row',
            ),

            html.Div(
                html.Table(className="responsive-table",
                      children=[
                          html.Thead(
                              html.Tr(
                                  children=[
                                      html.Th(col.title()) for col in df.columns.values],
                                  style={'color':'white', 'background-color': '#80bced', 'font-size': '110%'}
                                  )
                              ),
                          html.Tbody(
                              [
                                  
                              html.Tr(
                                  children=[
                                      html.Td(data) for data in d
                                      ], style={'color':'white', 'background-color': '#80bced', 'font-size': '80%'}
                                  )
                               for d in df.values.tolist()])
                          ]
                ),
                style = {"width": '95%',
                'margin-left': 'auto',
                'margin-right': 'auto'}
                ),
            ])]),

        dcc.Tab(label='Exploration & Analysis', 
            children=[

            # Title - Row
            html.Div(
                [
                    html.H4(
                        'Company Acquisitions by 7 Tech Giants',
                        style={"font-family": "Arial, sans-serif",
                               "font-weight": "bold",
                               'margin-top': '5',
                               "margin-bottom": "0"},
                        className='eight columns',
                    ),
                    html.A(html.Button('Code'), href='https://github.com/ginnyqg/dashboard', 
                        style = {
                                 'float': 'right',
                                 'margin-top': '5'
                                 }
                                 ),
                    # html.P('\u00A0\u00A0\u00A0', 
                    #     style = {'float': 'right',
                    #              'margin-top': '5'}),
                    html.A(html.Button('Data'), href='https://www.kaggle.com/shivamb/company-acquisitions-7-top-companies', 
                        style = {
                                 'float': 'right',
                                 'margin-top': '5'}),
                    html.H5(
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

            # Map, barchart, donut chart, word cloud, text
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
                    )
        ]),

        dcc.Tab(label='Table Details', 
            children=[

            # Title - Row
            html.Div(
                [
                    html.H4(
                        'Company Acquisitions by 7 Tech Giants',
                        style={"font-family": "Arial, sans-serif",
                               "font-weight": "bold",
                               'margin-top': '5',
                               'margin-bottom': '0'},
                        className='eight columns',
                    ),
                    html.H5(
                        'between 1987 and 2018',
                        style={'font-family': 'Arial, sans-serif',
                               "font-size": "120%",
                               "width": "80%",
                               "float": "left"
                               },
                        className='ten columns',
                    ),
                    html.A(html.Button('Export to csv'),
                        id='download-link',
                        download="acquisition_export.csv",
                        href="",
                        target="_blank",
                        style = {
                        'margin-top': '-10',
                        'float': 'right'
                        }
                    ),
                ],
                className='row'
            ),

            # # Selectors
            # html.Div(
            #     [
            #         html.Div(
            #             [
            #                 dcc.Checklist(
            #                         id = 'PComp2',
            #                         options=[
            #                             {'label': 'Google', 'value': 'Google'},
            #                             {'label': 'Microsoft', 'value': 'Microsoft'},
            #                             {'label': 'Facebook', 'value': 'Facebook'},
            #                             {'label': 'Apple', 'value': 'Apple'},
            #                             {'label': 'Twitter', 'value': 'Twitter'},
            #                             {'label': 'IBM', 'value': 'IBM'},
            #                             {'label': 'Yahoo', 'value': 'Yahoo'}
            #                         ],
            #                         values=['Google', 'Microsoft', 'Facebook', 'Apple', 'Twitter', 'IBM', 'Yahoo'],
            #                         labelStyle={'display': 'inline-block'}
            #                 ),
            #             ],
            #             className='twelve columns',
            #             style={
            #             # 'margin-top': '10',
            #                    'margin-bottom': '10'}
            #         ),
            #     ],
            #     className='row'
            # ),

            #table with details
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
                    style={
                        'font-family': 'Arial, sans-serif',
                        'font-size': "90%",
                        'margin-top': '10',
                        'margin-bottom': '10'},
                    className="twelve columns"
                    )
            ]),


        dcc.Tab(label='Conclusion', 
            children=[
            html.Div(
            [   
            html.H6("Analysis done by Gammadelt found that", style = {'font-family': 'Georgia', 'font-style': 'normal', 'color': 'black', 'background-color': 'white', 'margin-bottom': '30'}),    
            html.P("1. Google and Microsoft have the most acquisitions, but Microsoft takes the lead in the value of those acquisitions."),
            html.P("2. While Microsoft's acquired businesses are largely dominated by Software, Google's profile is a lot more diverse."),
            html.P("3. Majority of Google's acquisitions are in the Software and Mobile industry, but it also places high emphasis on Search, Advertising, Engine, Web, Video, Map, etc."),
            html.P("4. IBM and Facebook also follow a strategy of acquiring diverse businesses, although Facebook's focus is on applications of social media."),
            html.H6("In the end, this information will help Gammadelt evaluate its own business products and strategy, including its current assets, \
                how diverse or focused its lineup, and future development plans, and compare those to the types of businesses being acquired by the \
                tech giants to forecast who they may be acquired by in the future.", 
                style = {'font-family': 'Georgia', 'font-style': 'normal', 'color': 'black', 'background-color': 'white', 'margin-top': '30'})
            ],
            style = {
                        'font-family': 'Georgia',
                        'font-style': 'italic',
                        'color': 'white',
                        'background-color': '#8397e9',
                        'margin-top': '80',
                        'margin-bottom': '80'})
        ])
        ])
    ],
    style={
    'width': '90%',
    'fontFamily': 'Arial, sans-serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
}
)


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


#update datatable based on multi-select result, selected_row_indices
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


#export csv for datatable based on selection
@app.callback(
    Output('download-link', 'href'),
    [dash.dependencies.Input('datatable', 'rows')],
    [State('datatable', 'selected_row_indices')])
def update_download_link(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8, %EF%BB%BF" + urllib.parse.quote(csv_string)
    return csv_string



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
        width = 420,
        height = 260,
        margin = dict(
        l = 40,
        r = 40,
        b = 20,
        t = 70),
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
            "height": 350,
            "margin": {
            "l": 20,
            "r": 20,
            "b": 30,
            "t": 50},
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
                   width = 550,
                   height = 350,
                   margin = dict(
                    l = 20,
                    r = 20,
                    b = 30,
                    t = 30)
                          )

    return go.Figure(data=[trace], layout=layout)



# map-graph
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
            "l": 20,
            "r": 20,
            "b": 50,
            "t": 50},
            "geo": {
                "showframe": False,
                "showcoastlines": True,
                "projection": {
                "type": 'equirectangular'
                }
            }
        }
    }


# Callbacks and functions for map-graph
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





