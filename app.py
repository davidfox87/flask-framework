from flask import Flask, render_template
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

app = Flask(__name__)


def modify_doc(doc):
    df = sea_surface_temperature
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()

        source.data = data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    #doc.theme = Theme(filename="theme.yaml")


@app.route('/about')
def about():
  return render_template('about.html')



def modify_doc(doc):
    df = sea_surface_temperature
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()

        source.data = data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    #doc.theme = Theme(filename="theme.yaml")


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('https://limitless-forest-65059.herokuapp.com:5006/bkapp')
    return render_template("index.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["https://limitless-forest-65059.herokuapp.com:8000"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)








# def make_plot2():
#     #api_key = os.environ['MY_API_KEY']

#     #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={}'.format(api_key)
#     url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=0BQ5L9P8FFKF6MU1'
#     r = requests.get(url)
#     data = r.json()
#     df = pd.DataFrame(data)

#     df = df.iloc[6:]
#     df2 = df['Time Series (Daily)'].apply(pd.Series)
#     df2 = df2.astype('float64')
#     df2.index = pd.to_datetime(df2.index)

#     print(df2.info())
#     p = figure(title = "stock price", x_axis_type='datetime', sizing_mode="fixed", width=400, height=400)
#     p.line(df2.index, df2['4. close'], line_width=4)
#     print(df2.index.values, df2['4. close'].values)
#     return p







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