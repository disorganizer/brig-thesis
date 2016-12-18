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

LEGEND_MAP = {
    'aesread': 'AES/GCM [R]',
    'aeswrite': 'AES/GCM [W]',
    'chacharead': 'ChaCha20/Poly1305 [R]',
    'chachawrite': 'ChaCha20/Poly1305 [W]',
    'noneread': 'Base (no crypto) [R]',
    'nonewrite': 'Base (no crypto) [W]'
      }

LEGEND_SYS_MAP = {
    "Intel i5 (Go 1.7.1)": "Intel i5",
    "Intel i5 (Go 1.5.3)": "Intel i5",
    "Intel i5 (Go  1.6)": "Intel",
    "AMD Phenom II X4 (Go 1.5.3)": "AMD Phenom",
    "AMD Phenom II X4 (Go 1.7.1)": "AMD Phenom",
    "ARM11 (Go 1.7.1)": "RPi Zero",
    "Intel Atom N270 SSE2 (Go 1.7.1)": "Intel Atom",
    "Intel Atom N270 387fpu (Go 1.7.1)": "Intel Atom (387FPU)"
      }

def get_blocksizes(filesize):
    return [(2**x) for x in range(30) if 2**x >= 64 and (2**x)/1024**2 <= filesize]

# http://stackoverflow.com/questions/1094841/
# reusable-library-to-get-human-readable-version-of-file-size
def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

def render_line_plot_scrypt(data):
    line_chart = pygal.Line(
        legend_at_bottom=True,
        logarithmic=data["logarithmic"],
        style=pygal.style.LightSolarizedStyle,
        x_label_rotation=25,
        interpolate='cubic'
    )
    filesizes = set()

    plot_data = data["plot-data"]
    for item in plot_data:
        filesizes.add(item["filesize"])

    line_chart.title = data["title"]
    line_chart.x_labels = [pretty_size(x * 1024**2) for x in sorted(list(filesizes))]
    line_chart.x_title = data["x-title"]
    line_chart.y_title = data["y-title"]

    plot_data = sorted(plot_data, key=lambda d: d["system"],  reverse=False)
    print(plot_data)

    sys1 = [s for s in plot_data if s["system"] == "Intel Keygen (Go 1.7.1)" and s["kgfunc"] == "scrypt"]
    sys1 = sorted(sys1, key=lambda d: d["filesize"],  reverse=False)


    sys2 = [s for s in plot_data if s["system"] == "Intel Keygen (Go 1.7.1)" and s["kgfunc"] == "random"]
    sys2 = sorted(sys2, key=lambda d: d["filesize"],  reverse=False)

    sys3 = [s for s in plot_data if s["system"] == "Intel Keygen (Go 1.7.1)" and s["kgfunc"] == "none"]
    sys3 = sorted(sys3, key=lambda d: d["filesize"],  reverse=False)
    print(sys3)

    d1 = {}
    for item in sys1 + sys2 + sys3:
        d1.setdefault(item["kgfunc"], []).append(item["results"])

    for v in d1:
        line_chart.add(v, [round(x.pop()) for x in d1[v]])
        line_chart.render_to_file(data["outputfile"])

def format_min(values, min, filesize):
    values_str = []
    for v in values:
        val = str(v) + " ms; " + str(pretty_size((filesize) / (v/1000)) + "/s")
        if v == min:
            values_str.append("**" + val + "**")
        else:
            values_str.append(val)
    return values_str


def render_table(table, header, filesize):
    print("||" + "|".join([str(pretty_size(h)) + " [ms, B/s]" for h in header]) + "|")
    for title, row in table.items():
        print("|" + title + "|", end="")
        row = [999999 if v is None else v for v in row ]
        n = format_min(row, min(row), filesize)
        print("|".join(n))

def render_line_plot(data):
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

    table = {}
    plot_data = data["plot-data"]
    #print("|System|" + "|".join(x for x in line_chart.x_labels) + "|")
    header = get_blocksizes(data["needs"]["filesize"])
    for item in plot_data:
        avg_sec = mean(item["results"]) / 1000
        fs_bytes = megabytes_to_bytes(item["filesize"])
        avg_mb_sec = round(fs_bytes/avg_sec, 2)
        op = item["type"][0]
        #title =LEGEND_SYS_MAP[item["system"]] + "(" + LEGEND_MAP[item["encryption"] + item["type"]] + " (" + pretty_size(avg_mb_sec)  + "/s) [{0})".format(op.upper())
        title =LEGEND_SYS_MAP[item["system"]] + " (" + LEGEND_MAP[item["encryption"] + item["type"]]  + ")"
        #if item["filesize"] == 32:
        #    item["results"] += [None, None]
        table[title]= item["results"]
        line_chart.add(title, item["results"])
        line_chart.render_to_file(data["outputfile"])
    render_table(table, header, fs_bytes)

def megabytes_to_bytes(bytes):
    return bytes * 1024 ** 2

def render_bar_plot(data):
    line_chart = pygal.HorizontalBar(
        print_values=True,
        value_formatter=lambda x: '{}/s'.format(pretty_size(x)),
        truncate_legend=220,
        legend_at_bottom=True,
        logarithmic=data["logarithmic"],
        style=pygal.style.LightSolarizedStyle,
        x_label_rotation=60,
        y_label_rotation=300,
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
        # mbytes to bytes, and mseconds to seconds
        fs = item["filesize"] * 1024**2
        s = item["results"][10] / 1000
        d.setdefault(item["encryption"] + item["type"], []).append(fs/s)
        print(item["filesize"], min(item["results"])/1000)

    for k in sorted(d):
        line_chart.add(LEGEND_MAP[k], [round(v) for v in d[k]])
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

    if input_data["type"] == "scrypt":
        render_line_plot_scrypt(input_data)

    subprocess.call(
        ["inkscape", "{0}".format(input_data["outputfile"]),  "--export-pdf={0}.pdf".format(input_data["outputfile"])]
    )
    subprocess.call(
        ["chromium", "{0}".format(input_data["outputfile"]), "&"]
    )
