
// fetch('/plot')
//     .then(function(response) { return response.json(); })
//     .then(function(item) { Bokeh.embed.embed_item(item); })


// const response = await fetch('/plot')
// const item = await response.json()
// Bokeh.embed.embed_item(item)

// alert('hello')


// // create some data and a ColumnDataSource
// var x = Bokeh.LinAlg.linspace(-0.5, 20.5, 10);
// var y = x.map(function (v) { return v * 0.5 + 3.0; });
// var source = new Bokeh.ColumnDataSource({ data: { x: x, y: y } });
// // make the plot
// var plot = new Bokeh.Plot({
//    title: "BokehJS Plot",
//    plot_width: 400,
//    plot_height: 400
// });

// // add axes to the plot
// var xaxis = new Bokeh.LinearAxis({ axis_line_color: null });
// var yaxis = new Bokeh.LinearAxis({ axis_line_color: null });
// plot.add_layout(xaxis, "below");
// plot.add_layout(yaxis, "left");

// // add a Line glyph
// var line = new Bokeh.Line({
//    x: { field: "x" },
//    y: { field: "y" },
//    line_color: "#666699",
//    line_width: 2
// });
// plot.add_glyph(line, source);

// Bokeh.Plotting.show(plot);