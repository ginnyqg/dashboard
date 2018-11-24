
# coding: utf-8

# In[1]:


import plotly
plotly.tools.set_credentials_file(username = 'ginqg', api_key = 'IUSKOxkOgaDiEJMNeV0c')

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.dashboard_objs as dashboard
import plotly.plotly as py
import plotly.graph_objs as go
import cufflinks as cf


init_notebook_mode(connected=True)

import IPython.display
from IPython.display import Image

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

my_dboard = dashboard.Dashboard()
my_dboard.get_preview()


# In[2]:


raw = pd.read_csv("/Users/qinqingao/Desktop/Columbia/Courses/Fall 2018/APAN 5500 Viz/HW/A4/acquisitions.csv")


# In[3]:


# create bar chart: Count of acquisitions made by Top 7 Tech Companies

cnt_PC = pd.DataFrame({'PComp': raw.ParentCompany.value_counts()})
cnt_PC = cnt_PC.sort_values(by = 'PComp', ascending = False)

data  = go.Data([
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
    width = 400,
    height = 250,
    margin = dict(
    l = 40,
    r = 10,
    b = 40,
    t = 10),
#     title = '<b>Number of Acquisitions</b>',
#     xaxis = go.layout.XAxis(
#     title = 'Top 7 Tech Companies'
#     ),
    yaxis = go.layout.YAxis(
    title = 'Count'
    )
    )

fig  = go.Figure(data = data, layout = layout)
url_1 = py.plot(fig, filename = 'bar-plot-cnt-PComp', auto_open = False)
py.iplot(fig, filename = 'bar-plot-cnt-PComp')


# In[4]:


# # create horizontal bar chart: Amount of Value (USD) acquired by Top 7 Tech Companies

# amt_PC = pd.DataFrame(raw.groupby(['ParentCompany'])['Value (USD)'].sum())
# amt_PC = amt_PC.sort_values(by = 'Value (USD)', ascending = True)


# data  = go.Data([
#                 go.Bar(
#                 x = amt_PC['Value (USD)'], 
#                 y = amt_PC.index,
#                 text = round(amt_PC['Value (USD)']/1000000000, 2),
#                 textposition = 'outside',
#                 marker = dict(
#                         color = '#b8e5dd',
#                         line = dict(
#                         color = '#b8e5dd',
#                         width = 1.5)
#                         ),
#                 opacity = 0.8,
#                 orientation ='h'
#         )])

# layout = go.Layout(
#     width = 1000,
#     height = 500,
#     title = "<b>Amount of Acquisition (USD) by Top 7 Tech Companies</b>",
#     yaxis = go.layout.YAxis(
#     title = 'Value (USD, $B)'
#     ))

# fig  = go.Figure(data = data, layout = layout)
# url_2 = py.plot(fig, filename = 'hbar-plot-amt-PComp', auto_open = False)
# py.iplot(fig, filename = 'hbar-plot-amt-PComp')


# In[5]:


# create donut chart: Amount of Value (USD) acquired by Top 7 Tech Companies

amt_PC = pd.DataFrame(raw.groupby(['ParentCompany'])['Value (USD)'].sum())
amt_PC = amt_PC.sort_values(by = 'Value (USD)', ascending = True)

fig = {
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
#         "title":"<b>Value of Acquisition (US$B)</b>",
#         "autosize": False,
        "width": 300,
        "height": 300,
        "margin": {
        "l": 10,
        "r": 10,
        "b": 10,
        "t": 10},
        "annotations": [
            {
                "font": {
                    "size": 12
                },
                "showarrow": False,
                "text": "Top 7",
                "x": 0.5,
                "y": 0.5
            }
        ]
    }
}


url_2 = py.plot(fig, filename = 'donut', auto_open = False)
py.iplot(fig, filename = 'donut')


# In[6]:


# create world map

# csl = [[1,"rgb(5, 10, 172)"],[0.75,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
#        [0.25,"rgb(90, 120, 245)"],[0.15,"rgb(106, 137, 247)"],[0,"rgb(220, 220, 220)"]]

csl = [[0, 'rgb(255, 255, 255)'], [0.0005, 'rgb(255, 243, 234)'], [0.001, 'rgb(255, 230, 208)'], [0.01, 'rgb(255, 175, 106)'], [0.05, 'rgb(255, 161, 81)'], [0.25, 'rgb(255, 134, 30)'], [1, 'rgb(255, 118, 0)']]


data = [dict(
        type = 'choropleth',
        locations = raw['Country'],
        z = raw['Value (USD)'],
#         text = raw['Country'],
        colorscale = csl,
#         colorscale = 'Rainbow',
        autocolorscale = False,
        showscale = False,
        marker = dict(
                line = dict (
                color = 'rgb(180,180,180)',
                width = 1
            )),
#         tick0 = 0,
        zmin = 0,
#         dtick = 1000,
        colorbar = dict(
            title = 'US$ B'
        )
        )
       ]

layout = dict(
#     title = '<b>Worldwide Acquisition Value</b>',
    width = 800,
    height = 450,
    margin = dict(
    l = 10,
    r = 10,
    b = 10,
    t = 10),
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
        type = 'equirectangular'
        )
    )
)

fig = dict(data = data, layout = layout)

url_3 = py.plot(fig, filename='world-map', auto_open=False)
py.iplot(fig, filename='world-map')


# In[7]:


from wordcloud import WordCloud, STOPWORDS

def plotly_wordcloud(text):
    wc = WordCloud(stopwords = set(STOPWORDS),
                   max_words = 200,
                   max_font_size = 100)
    wc.generate(text)
    
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
    
    trace = go.Scatter(x=x, 
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
                       width = 600,
                       height = 400,
                       margin = dict(
                        l = 5,
                        r = 5,
                        b = 5,
                        t = 5)
                              )
    
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig

text = raw.Business

url_4 = py.plot(plotly_wordcloud(str(text)), filename='word-cloud', auto_open=False)
py.iplot(plotly_wordcloud(str(text)), filename='word-cloud')


# In[8]:


import re

def fileId_from_url(url):
    """Return fileId from a url."""
    raw_fileId = re.findall("~[A-z]+/[0-9]+", url)[0][1: ]
    return raw_fileId.replace('/', ':')

def sharekey_from_url(url):
    """Return the sharekey from a url."""
    if 'share_key=' not in url:
        return "This url is not 'sercret'. It does not have a secret key."
    return url[url.find('share_key=') + len('share_key='):]

fileId_1 = fileId_from_url(url_1)
fileId_2 = fileId_from_url(url_2)
fileId_3 = fileId_from_url(url_3)
fileId_4 = fileId_from_url(url_4)


text_for_box = """ 
This is a dashboard showing company acquisition data for the top 7 tech companies: 
[Google](https://abc.xyz/investor/), [Microsoft](https://www.microsoft.com/en-us/investor), [Facebook](https://investor.fb.com/home/default.aspx), [Apple](https://investor.apple.com/investor-relations/default.aspx), [Yahoo](https://finance.yahoo.com/), [Twitter](https://investor.twitterinc.com/investor-relations), [IBM](https://www.ibm.com/investor/)


###### Geo map
1. Showing ...
2. Explanation ...

###### Bar chart
1. Showing ...
2. Explanation ...

###### Donut chart
1. Showing ...
2. Explanation ...

###### Viz 4
1. Showing ...
2. Explanation ...

More information about the data can be found [here](https://www.kaggle.com/shivamb/company-acquisitions-7-top-companies).
"""


box_a = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_3,
    'title': 'Worldwide Acquisition Value'
}

box_b = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_2,
    'title': 'Value of Acquisition (US$ B)'
}


box_c = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_1,
    'title': 'Number of Acquisitions'
}

box_d = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_4,
    'title': 'Type of Businesses Acquired'
}

box_e = {
    'type': 'box',
    'boxType': 'text',
    'text': text_for_box,
    'title': 'Background & Notes'
}


# In[9]:


# insert modules

my_dboard.insert(box_a)

my_dboard.insert(box_b, 'right', 1, fill_percent = 30)

my_dboard.insert(box_c, 'below', 1)

my_dboard.insert(box_d, 'right', 2)

my_dboard.insert(box_e, 'below', 4)

my_dboard.get_preview()


# In[10]:


my_dboard['settings']['title'] = 'Tech Company Acquisition Dashboard'


# In[11]:


# my_dboard['settings']['logoUrl'] = 'https://images.plot.ly/language-icons/api-home/python-logo.png'

my_dboard['settings']['links'] = []
my_dboard['settings']['links'].append({'title': 'Github', 'url': 'https://github.com/ginnyqg'})
my_dboard['settings']['links'].append({'title': 'Website', 'url': 'https://ginnyqg.github.io'})


# In[12]:


my_dboard['settings']['foregroundColor'] = '#000000'
my_dboard['settings']['backgroundColor'] = '#F4F7FB'
my_dboard['settings']['headerForegroundColor'] = '#ffffff'
my_dboard['settings']['headerBackgroundColor'] = '#4E87C2'
my_dboard['settings']['boxBackgroundColor'] = '#ffffff'
my_dboard['settings']['boxBorderColor'] = '#ffffff'
my_dboard['settings']['boxHeaderBackgroundColor'] = '#ffffff'


my_dboard['settings']['fontFamily'] = 'Raleway'
my_dboard['settings']['headerFontSize'] = '2.4em'
my_dboard['settings']['headerFontWeight'] = '600'


# In[13]:


stacked_dboard = dashboard.Dashboard()
text_box = {
    'type': 'box',
    'boxType': 'text',
    'text': 'empty space'
}
for _ in range(5):
    stacked_dboard.insert(text_box, 'below', 1)

# stacked_dboard.get_preview()


# In[14]:


stacked_dboard['layout']['size'] = 2400
# stacked_dboard['layout']['height'] = 500
# stacked_dboard['layout']['width'] = 1000


# In[15]:


py.dashboard_ops.upload(my_dboard, 'Tech Company Acquisition Dashboard')

