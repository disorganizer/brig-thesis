#!/usr/bin/env python
# encoding: utf-8

import json
import os
import sys
import pygal
import pygal.style
from collections import OrderedDict
from collections import defaultdict
from math import log
from statistics import mean
import subprocess
import pprint


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
    line_chart.x_labels = [pretty_size(x) for x in get_blocksizes(data["needs"]["filesize"])]
    line_chart.x_title = data["x-title"]
    line_chart.y_title = data["y-title"]

    plot_data = data["plot-data"]

    for item in plot_data:
        avg = mean(item["results"])
        avg = round(data["needs"]["filesize"]/(avg/(1024**3)), 2)
        title = item["title"] + " (" + pretty_size(avg)  + "/s)"
        line_chart.add(title, item["results"])
        line_chart.render_to_file(data["outputfile"])

def render_bar_plot(data):
    pygal.style.LightSolarizedStyle.background = "#FFFFFF"
    pygal.style.LightSolarizedStyle.plot_background = "#FFFFFF"

    line_chart = pygal.Bar(
        order_min=1,
        legend_at_bottom=True,
        logarithmic=data["logarithmic"],
        style=pygal.style.LightSolarizedStyle,
        x_label_rotation=25,
        interpolate='cubic'
    )
    line_chart.title = data["title"]

    plot_data = data["plot-data"]
    plot_data = sorted(plot_data, key=lambda d: d["system"] + d["encryption"] + d["type"], reverse=False)

    line_chart.x_labels = list(sorted(set([x["system"] for x in plot_data])))
    line_chart.x_title = data["x-title"]
    line_chart.y_title = data["y-title"]

    d = {}
    for item in plot_data:
        d.setdefault(item["encryption"] + "/" + item["type"], []).append(
            item["filesize"]/(min(item["results"])/1000/1000)
        )

    for k in sorted(d):
        line_chart.add(k, [round(v/1024) for v in d[k]])
        line_chart.render_to_file(data["outputfile"])


def is_valid(jdir, metadata):
    if jdir.get("system") not in metadata["needs"]["system"]:
        return False

    if jdir.get("type") not in metadata["needs"]["type"]:
        return False

    #if jdir.get("filesize") != metadata["needs"]["filesize"]:
    #    return False

    if jdir.get("encryption") not in metadata["needs"]["algo"]:
        return False

    return True

def get_input_data(path):
    with open(path, 'r') as fd:
        metadata = json.loads(fd.read())
        metadata["input-data"] = os.path.abspath(metadata["input-data"])

    # Load all benchmark files
    benchmark_files = []
    for file in sorted(os.listdir(metadata["input-data"])):
        jfile = os.path.abspath(os.path.join(metadata["input-data"], file))
        if not os.path.isdir(jfile) and jfile.endswith("json"):
            with open(jfile, "r") as fd:
                benchmark_files.append(json.loads(fd.read()))

    # Filter only needed files
    needed_files = []
    for jfile in benchmark_files:
        if is_valid(jfile, metadata):
            metadata["plot-data"].append(jfile)
    return metadata

if __name__ == '__main__':
    config_path = os.path.abspath(sys.argv[1])
    dir_path = os.path.dirname(config_path)
    input_data = get_input_data(config_path)
    input_data["outputfile"] = os.path.join(dir_path, os.path.basename(config_path) + ".svg")

    if input_data["plot-data"] == []:
        print("No Plot data found with this attributes.")
        sys.exit(0)

    #with open('/tmp/input.json', "w") as fd:
    #    fd.write(json.dumps(input_data))
    #    sys.exit(-1)
    if input_data["type"] == "line":
        render_line_plot(input_data)

    if input_data["type"] == "bar":
        render_bar_plot(input_data)

    subprocess.call(
        ["inkscape", "{0}".format(input_data["outputfile"]),  "--export-pdf={0}.pdf".format(input_data["outputfile"])]
    )
    subprocess.call(
        ["chromium", "{0}".format(input_data["outputfile"]), "&"]
    )
