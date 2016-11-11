#!/usr/bin/env python
# encoding: utf-8

import json
import sys
import pygal
import pygal.style
from math import log
from statistics import mean
import subprocess

FILESIZE=128
BLOCKSIZES = [(2**x) for x in range(30) if 2**x >= 64 and (2**x)/1024**2 <= FILESIZE]


# http://stackoverflow.com/questions/1094841/
# reusable-library-to-get-human-readable-version-of-file-size
def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

def render_plot(*args, logarithmic=True):
    pygal.style.LightSolarizedStyle.background = "#FFFFFF"
    pygal.style.LightSolarizedStyle.plot_background = "#FFFFFF"

    line_chart = pygal.Line(
        legend_at_bottom=True,
        logarithmic=logarithmic,
        style=pygal.style.LightSolarizedStyle,
        x_label_rotation=25,
        interpolate='cubic'
    )
    line_chart.title = "Write benchmark of crypto layer."
    line_chart.x_labels = [pretty_size(x) for x in BLOCKSIZES]
    line_chart.x_title = "MaxBlockSize of encryption layer in bytes."
    line_chart.y_title = "Time in milliseconds"
    for arg in args:
        #print(arg["title"], arg["results"])
        print(arg["results"])
        avg = mean(arg["results"])
        avg = round(FILESIZE/(avg/(1024**3)), 2)
        print(avg)
        title = arg["title"] + " (" + pretty_size(avg)  + "/s)"
        line_chart.add(title, arg["results"])
    line_chart.render_to_file('render.svg')


if __name__ == '__main__':
    data = []
    for item in sys.argv[1:]:
        with open(item, "r") as fd:
            data.append(json.loads(fd.read()))
    render_plot(*data)
    subprocess.call(["inkscape", "./render.svg",  "--export-pdf=render.svg.pdf"])
