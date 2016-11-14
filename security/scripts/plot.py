#!/usr/bin/env python
# encoding: utf-8

import json
import os
import sys
import pygal
import pygal.style
from collections import OrderedDict
from math import log
from statistics import mean
import subprocess


def get_blocksizes(filesize):
    return [(2**x) for x in range(30) if 2**x >= 64 and (2**x)/1024**2 <= filesize]

# http://stackoverflow.com/questions/1094841/
# reusable-library-to-get-human-readable-version-of-file-size
def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

def render_line_plot(data):
    pygal.style.LightSolarizedStyle.background = "#FFFFFF"
    pygal.style.LightSolarizedStyle.plot_background = "#FFFFFF"

    line_chart = pygal.Line(
        legend_at_bottom=True,
        logarithmic=data["logarithmic"],
        style=pygal.style.LightSolarizedStyle,
        x_label_rotation=25,
        interpolate='cubic'
    )
    line_chart.title = data["title"]
    line_chart.x_labels = [x for x in get_blocksizes(data["filesize"])]
    line_chart.x_title = data["x-title"]
    line_chart.y_title = data["y-title"]

    plot_data = data["plot-data"]

    for item in plot_data:
        print(item)
        avg = mean(item["results"])
        avg = round(data["filesize"]/(avg/(1024**3)), 2)
        title = item["title"] + " (" + pretty_size(avg)  + "/s)"
        line_chart.add(title, item["results"])
        line_chart.render_to_file(data["outputfile"])

def extract_plot_data(data, fs):
    algos = set()
    systems = set()

    for item in data:
        algos.add(item["encryption"])
        systems.add(item["system"])
    d = {a:{s: None for s in systems} for a in algos}

    for item in data:
        algo = item["encryption"]
        sys = item["system"]
        d[algo][sys] = fs/(min(item["results"])/1024**3)
    d["systems"] = systems
    return d



#def render_bar_plot(data):
#    pygal.style.LightSolarizedStyle.background = "#FFFFFF"
#    pygal.style.LightSolarizedStyle.plot_background = "#FFFFFF"
#
#    line_chart = pygal.Bar(
#        legend_at_bottom=True,
#        logarithmic=data["logarithmic"],
#        style=pygal.style.LightSolarizedStyle,
#        x_label_rotation=25,
#        interpolate='cubic'
#    )
#    line_chart.title = data["title"]
#
#    plot_data = data["plot-data"]
#    d = extract_plot_data(plot_data, data["filesize"])
#    #line_chart.x_labels = []
#    #algos = set()
#    line_chart.x_labels = d["systems"]
#    line_chart.x_title = data["x-title"]
#    line_chart.y_title = data["y-title"]
#
#    #mapping = {k: None for k in algos}
#    #for k, v in mapping.items():
#    #    mapping[k] = OrderedDict({sys:None for sys in line_chart.x_labels})
#
#    #for item in plot_data:
#    #    algo = item["encryption"]
#    #    mapping[algo][item["system"]] = max(item["results"])
#
#    #print(mapping["none"].values())
#    for k,v in d.items():
#        print(v.pop())
#        line_chart.add(k, [3])
#        line_chart.render_to_file(data["outputfile"])

def get_input_data(path):
    with open(path, 'r') as fd:
        return json.loads(fd.read())


if __name__ == '__main__':
    config_path = os.path.abspath(sys.argv[1])
    dir_path = os.path.dirname(config_path)
    print(config_path)
    input_data = get_input_data(config_path)
    input_data["outputfile"] = os.path.join(dir_path, input_data.get("outputfile"))

    for item in input_data["input"]:
        with open(os.path.join(dir_path,item), "r") as fd:
            input_data["plot-data"].append(json.loads(fd.read()))

    if input_data["type"] == "line":
        render_line_plot(input_data)

    #if input_data["type"] == "bar":
    #    render_bar_plot(input_data)

    subprocess.call(
        ["inkscape", "{0}".format(input_data["outputfile"]),  "--export-pdf={0}.pdf".format(input_data["outputfile"])]
    )
