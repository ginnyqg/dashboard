
# coding: utf-8

# In[1]:


import plotly
plotly.tools.set_credentials_file(username = 'gqgg', api_key = 'Jj0cizKNthtkBLZAvBrP')

import plotly.dashboard_objs as dashboard
import plotly.plotly as py
import plotly.graph_objs as go
import cufflinks as cf

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



import plotly.plotly as py
import plotly.graph_objs as go

cnt_PC = pd.DataFrame({'PComp': raw.ParentCompany.value_counts()})
cnt_PC = cnt_PC.sort_values(by = 'PComp', ascending = False)

data  = go.Data([
                go.Bar(
                x = cnt_PC.index,
                y = cnt_PC.PComp,
                text = cnt_PC.PComp,
                textposition = 'outside',
                marker = dict(
                        color = 'orange',
                        line = dict(
                        color = 'orange',
                        width = 1.5)
                        ),
                opacity = 0.6
        )])

layout = go.Layout(
    width = 800,
    height = 500,
    title = "<b>Acquisitions by Top 7 Tech Companies</b>",
    yaxis = go.layout.YAxis(
    title = 'Count'
    ))

fig  = go.Figure(data = data, layout = layout)
url_1 = py.plot(fig, filename = 'bar-plot-cnt-PComp', auto_open = False)
py.iplot(fig, filename = 'bar-plot-cnt-PComp')


# cnt_PC = raw.ParentCompany.value_counts()
# cnt_PC.iplot(kind='bar', yTitle='Count', title='Acquisitions by Top 7 Tech Companies',
#              filename='bar-plot-cnt-PComp_2')


# In[4]:


# # create horizontal chart: Amount of Value (USD) acquired by Top 7 Tech Companies

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


amt_PC = pd.DataFrame(raw.groupby(['ParentCompany'])['Value (USD)'].sum())
amt_PC = amt_PC.sort_values(by = 'Value (USD)', ascending = True)

fig = {
  "data": [
    {
      "values": amt_PC['Value (USD)'],
      "labels": amt_PC.index,
      "domain": {"x": [0, 1]},
      "hoverinfo":"label",
      "hole": .4,
      "type": "pie"
    }],
  "layout": {
        "title":"<b>Amount of Acquisition (USD) by Top 7 Tech Companies</b>",
        "annotations": [
            {
                "font": {
                    "size": 20
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


x0 = np.random.randn(50)
x1 = np.random.randn(50) + 2
x2 = np.random.randn(50) + 4
x3 = np.random.randn(50) + 6

colors = ['#FAEE1C', '#F3558E', '#9C1DE7', '#581B98']

trace0 = go.Box(x=x0, marker={'color': colors[0]})
trace1 = go.Box(x=x1, marker={'color': colors[1]})
trace2 = go.Box(x=x2, marker={'color': colors[2]})
trace3 = go.Box(x=x3, marker={'color': colors[3]})
data = [trace0, trace1, trace2, trace3]

url_3 = py.plot(data, filename='box-plots-for-dashboard_2', auto_open=False)
py.iplot(data, filename='box-plots-for-dashboard_2')


# In[7]:


x0 = np.random.randn(50)
x1 = np.random.randn(50) + 2
x2 = np.random.randn(50) + 4
x3 = np.random.randn(50) + 6

colors = ['#FAEE1C', '#F3558E', '#9C1DE7', '#581B98']

trace0 = go.Box(x=x0, marker={'color': colors[0]})
trace1 = go.Box(x=x1, marker={'color': colors[1]})
trace2 = go.Box(x=x2, marker={'color': colors[2]})
trace3 = go.Box(x=x3, marker={'color': colors[3]})
data = [trace0, trace1, trace2, trace3]

url_4 = py.plot(data, filename='box-plots-for-dashboard_3', auto_open=False)
py.iplot(data, filename='box-plots-for-dashboard_3')


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
#### Background 
This is a dashboard showing company acquisition data for the top 7 tech companies: 
[Google](https://abc.xyz/investor/), [Microsoft](https://www.microsoft.com/en-us/investor), [Facebook](https://investor.fb.com/home/default.aspx), [Apple](https://investor.apple.com/investor-relations/default.aspx), [Yahoo](https://finance.yahoo.com/), [Twitter](https://investor.twitterinc.com/investor-relations), [IBM](https://www.ibm.com/investor/)


#### Viz 1
1. Showing ...
2. Explanation ...


#### Viz 2
1. Showing ...
2. Explanation ...


More information about the data can be found [here](https://www.kaggle.com/shivamb/company-acquisitions-7-top-companies).
"""


box_a = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_1,
    'title': ''
}

box_b = {
    'type': 'box',
    'boxType': 'text',
    'text': text_for_box,
    'title': 'Background & Notes'
}


box_c = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_2,
    'title': ''
}

box_d = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_3,
    'title': ''
}

box_e = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fileId_4,
    'title': ''
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


# In[15]:


py.dashboard_ops.upload(my_dboard, 'Tech Company Acquisition Dashboard')

