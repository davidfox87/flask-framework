from flask import Flask, render_template, request, redirect, jsonify, url_for

from bokeh.embed import components
from bokeh.models.callbacks import CustomJS
from bokeh.models import ColumnDataSource, Slider, Select, TextInput,  \
    Button, DateRangeSlider, CrosshairTool, PreText, HoverTool, CheckboxButtonGroup, RadioButtonGroup
from bokeh.layouts import column, row
from bokeh.embed import json_item
from bokeh.plotting import figure

import numpy as np
import pandas as pd
import json

import requests
import os
import jinja2

from dotenv import load_dotenv
load_dotenv()  
#from boto.s3.connection import S3Connection


app = Flask(__name__)
app.config["DEBUG"] = True

def get_data(name="IBM"):
    print(os.environ.get('API_KEY'), 'HELLLLLLO!!!!!!!!!!!!!!!!!')
    print('HELLOOOOOOOO!!!!!!!!')
    alphav_key = os.environ.get('API_KEY')
    # print("The alpha vantage api key is {}".format(alphav_key))
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}'.format(name, alphav_key)
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data)

    df = df.iloc[6:]
 
    df2 = df['Time Series (Daily)'].apply(pd.Series)
    df2 = df2.astype('float64')
    df2.index = pd.to_datetime(df2.index)
    df2=df2.loc[:,["4. close"]]

    return df2

@app.route('/<stock>')
@app.route('/')
def index(stock="IBM"):

    # Set y-axis defaults
    df = get_data(stock)

    df['y'] = df["4. close"]
  
    source = ColumnDataSource(data=df)
    source2 = ColumnDataSource(data=df)

    hover = HoverTool(tooltips=[('date', '@index{%F}'), ('Value', '@y')],
          formatters={'@index' : 'datetime'})

    # # Create the default plot figure
    fig = figure(title = "stock price", x_axis_type='datetime', plot_width=600, plot_height=200, sizing_mode="stretch_width")
    fig.line(source=source, x='index', y='y')
    fig.add_tools(hover)
    fig.add_tools(CrosshairTool())
    stats = PreText(text='', width=500)
    stats.text = str(df["4. close"].describe())
    # # define dropdown box widget
    
    date_range_slider = DateRangeSlider(title="date_range", start=source.data['index'][-1], 
        end=source.data['index'][0], value=(source.data['index'][-1], source.data['index'][0]), step=1, width=300)

    # define what do when widget changes
    callback = CustomJS(args=dict(source=source, ref_source=source2), code="""
        // print out array of date from, date to
        // console.log(cb_obj.value); 
    
        // dates returned from slider are not at round intervals and include time;
        const date_from = Date.parse(new Date(cb_obj.value[0]).toDateString());
        const date_to = Date.parse(new Date(cb_obj.value[1]).toDateString());

        const data = source.data;
        const ref = ref_source.data;

        //using for loop
        // for each element x in xs, do something
        // xs.forEach((x, i) => console.log(x));

        // Creating new Array and appending correctly parsed dates
        let new_ref = []
        ref["index"].forEach(elem => {
            elem = Date.parse(new Date(elem).toDateString());
            new_ref.push(elem);
        })

        // Creating Indices with new Array
        const from_pos = new_ref.indexOf(date_from);
        const to_pos = new_ref.indexOf(date_to) + 1;

        // re-create the source data from "reference"
        if (to_pos != -1 && from_pos != -1) {
          data["y"] = ref["y"].slice(to_pos, from_pos);
          data["index"] = ref["index"].slice(to_pos, from_pos);

          source.change.emit();
        }

    """)

    

    checkbox = RadioButtonGroup(labels=["1M", "3M", "6M", "1Y"], active=0)
    callback_checkbox = CustomJS(args=dict(source=source), code="""
        console.log("Button clicked"); 

        const data = source.data;
        const new_data = {index: [], y: []};

        if (cb_obj.active==0) {
          new_data["y"] = data["y"].slice(0, 30);
          new_data["index"] = data["index"].slice(0, 30);
        } 
        if (cb_obj.active==1) {
          new_data["y"] = data["y"].slice(0, 90);
          new_data["index"] = data["index"].slice(0, 90);
        } 

        if (cb_obj.active==2) {
          new_data["y"] = data["y"].slice(0, 183);
          new_data["index"] = data["index"].slice(0, 183);
        } 

         if (cb_obj.active==3) {
          new_data["y"] = data["y"].slice(0, 365);
          new_data["index"] = data["index"].slice(0, 365);
        } 

        source.data = new_data

        source.change.emit();
        
     """)

    checkbox.js_on_click(callback_checkbox)

    button = Button(label = "Click on the button",
                button_type = "danger")
  
    callback_button = CustomJS(args=dict(source=source), code="""
        console.log("Button clicked"); 

        const data = source.data;

        const new_data = {index: [], y: []};

        new_data["y"] = data["y"].slice(0, 60);
        new_data["index"] = data["index"].slice(0, 60);

        source.data = new_data

        source.change.emit();
        
     """)

    button.js_on_click(callback_button)

    date_range_slider.js_on_change('value', callback)

    date_range_slider.sizing_mode = 'scale_width'
    stats.sizing_mode = 'scale_width'

    inputs_column = column([date_range_slider, checkbox, fig, stats], width=50, height=500)
    inputs_column.sizing_mode = 'scale_width'

    script, div = components(inputs_column)

    return render_template('index.html', plot_script=script,
        plot_div=div, text=stock)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
  if request.method == 'POST':
    name = request.form['stock_name']

    return redirect(url_for('index',stock=name))



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