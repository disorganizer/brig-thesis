#!/usr/bin/env python
# encoding: utf-8

import json
import sys
import pygal
import pygal.style

BLOCKSIZES = [
    128, 512, 1024, 4096, 32768, 65536, 131072, 262144, 524288,
    1048576, 2097152, 4194304, 8388608,
]

def render_plot(*args, logarithmic=True):
    pygal.style.LightSolarizedStyle.background = "#FFFFFF"
    pygal.style.LightSolarizedStyle.plot_background = "#FFFFFF"

    line_chart = pygal.Line(
        legend_at_bottom=True,
        logarithmic=logarithmic,
        style=pygal.style.LightSolarizedStyle,
        interpolate='cubic'
    )
    line_chart.title = "Read benchmark of crypto layer."
    line_chart.x_labels = [x if x < 1024 else str(int(x/1024)) + "K" for x in BLOCKSIZES]
    line_chart.x_title = "Blocksize in bytes."
    line_chart.y_title = "Time in milliseconds"
    for arg in args:
        print(arg["title"], arg["results"])
        line_chart.add(arg["title"], arg["results"])
    line_chart.render_to_file('render.svg')


if __name__ == '__main__':
    data = []
    for item in sys.argv[1:]:
        with open(item, "r") as fd:
            data.append(json.loads(fd.read()))
    render_plot(*data)
