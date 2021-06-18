from flask import Flask, render_template, request, redirect

import numpy as np
import pandas as pd
import json

import requests
from dotenv import load_dotenv
import os

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.sampledata.iris import flowers

load_dotenv()
#api_key = os.environ['MY_API_KEY']

app = Flask(__name__)

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

def make_plot(x, y):
    p = figure(title = "Iris Morphology", sizing_mode="fixed", width=400, height=400)
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
    return p

def make_plot2():
    api_key = os.environ['MY_API_KEY']

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={}'.format(api_key)
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data)

    df = df.iloc[6:]
    df2 = df['Time Series (Daily)'].apply(pd.Series)
    df2 = df2.astype('float64')
    df2.index = pd.to_datetime(df2.index)

    print(df2.info())
    p = figure(title = "stock price", x_axis_type='datetime', sizing_mode="fixed", width=400, height=400)
    p.line(df2.index, df2['4. close'], line_width=4)
    print(df2.index.values, df2['4. close'].values)
    return p


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/plot')
def plot():
    # p = make_plot('sepal_width', 'sepal_length')
    p = make_plot2()
    return json.dumps(json_item(p))


if __name__ == '__main__':
  #app.run(port=33507)
  app.run()






# from __future__ import print_function
# import json

# from bokeh.embed import json_item
# from bokeh.plotting import figure
# from bokeh.resources import CDN
# from bokeh.sampledata.iris import flowers

# from flask import Flask
# from jinja2 import Template

# app = Flask(__name__)

# page = Template("""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   {{ resources }}
# </head>
# <body>
#   <div id="myplot"></div>
#   <div id="myplot2"></div>
#   <script>
#   fetch('/plot')
#     .then(function(response) { return response.json(); })
#     .then(function(item) { Bokeh.embed.embed_item(item); })
#   </script>
#   <script>
#   fetch('/plot2')
#     .then(function(response) { return response.json(); })
#     .then(function(item) { Bokeh.embed.embed_item(item, "myplot2"); })
#   </script>
# </body>
# """)

# colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
# colors = [colormap[x] for x in flowers['species']]

# def make_plot(x, y):
#     p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400)
#     p.xaxis.axis_label = x
#     p.yaxis.axis_label = y
#     p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
#     return p

# @app.route('/')
# def root():
#     return page.render(resources=CDN.render())

# @app.route('/plot')
# def plot():
#     p = make_plot('petal_width', 'petal_length')
#     return json.dumps(json_item(p, "myplot"))

# @app.route('/plot2')
# def plot2():
#     p = make_plot('sepal_width', 'sepal_length')
#     return json.dumps(json_item(p))

# if __name__ == '__main__':
#     app.run()