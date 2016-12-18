# Anhang E: Benchmarktool und Skripte {#sec:APP_SCRIPTE}

~~~go
package main

import (
	"crypto/rand"
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"time"

	"github.com/disorganizer/brig/store/compress"
	"github.com/disorganizer/brig/store/encrypt"
	"golang.org/x/crypto/scrypt"
)

const (
	aeadCipherChaCha = iota
	aeadCipherAES
)

type options struct {
	zipalgo           string
	encalgo           string
	keyderiv          string
	output            string
	args              []string
	write             bool
	read              bool
	maxblocksize      int64
	useDevNull        bool
	forceDstOverwrite bool
}

func withTime(fn func()) time.Duration {
	now := time.Now()
	fn()
	return time.Since(now)
}

func openDst(dest string, overwrite bool) *os.File {
	if !overwrite {
		if _, err := os.Stat(dest); !os.IsNotExist(err) {
			log.Fatalf("Opening destination failed, %v exists.\n", dest)
		}
	}

	fd, err := os.OpenFile(dest, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0755)
	if err != nil {
		log.Fatalf("Opening destination %v failed: %v\n", dest, err)
	}
	return fd
}

func openSrc(src string) *os.File {
	fd, err := os.Open(src)
	if err != nil {
		log.Fatalf("Opening source %v failed: %v\n", src, err)
	}
	return fd
}

func dstFilename(compressor bool, src, algo string) string {
	if compressor {
		return fmt.Sprintf("%s.%s", src, algo)
	}
	return fmt.Sprintf("%s.%s", src, "uncompressed")
}

func dieWithUsage() {
	fmt.Printf("Usage of %s:\n", os.Args[0])
	flag.PrintDefaults()
	os.Exit(-1)

}

func die(err error) {
	log.Fatal(err)
	os.Exit(-1)
}

func parseFlags() options {
	read := flag.Bool("r", false, "Read mode.")
	write := flag.Bool("w", false, "Write mode.")
	maxblocksize := flag.Int64("b", 64*1024, "BlockSize.")
	zipalgo := flag.String("c", "none", "Possible compression algorithms: none, snappy, lz4.")
	output := flag.String("o", "", "User defined output file destination.")
	encalgo := flag.String("e", "aes", "Possible encryption algorithms: aes, chacha.")
	keyderiv := flag.String("k", "none", "Use random or scrypt as key derivation: random, scrypt")
	forceDstOverwrite := flag.Bool("f", false, "Force overwriting destination file.")
	useDevNull := flag.Bool("D", false, "Write to /dev/null.")
	flag.Parse()
	return options{
		read:              *read,
		write:             *write,
		zipalgo:           *zipalgo,
		encalgo:           *encalgo,
		output:            *output,
		keyderiv:          *keyderiv,
		maxblocksize:      *maxblocksize,
		forceDstOverwrite: *forceDstOverwrite,
		useDevNull:        *useDevNull,
		args:              flag.Args(),
	}
}

func derivateAesKey(pwd, salt []byte, keyLen int) []byte {
	key, err := scrypt.Key(pwd, salt, 16384, 8, 1, keyLen)
	if err != nil {
		panic("Bad scrypt parameters: " + err.Error())
	}
	return key
}

func main() {
	opts := parseFlags()
	if len(opts.args) != 1 {
		dieWithUsage()
	}
	if opts.read && opts.write {
		dieWithUsage()
	}
	if !opts.read && !opts.write {
		dieWithUsage()
	}

	srcPath := opts.args[0]
	algo, err := compress.FromString(opts.zipalgo)
	if err != nil {
		die(err)
	}

	src := openSrc(srcPath)
	defer src.Close()

	if opts.useDevNull && opts.output != "" {
		fmt.Printf("%s\n", "dev/null (-D) and outputfile (-o) may not be set at the same time.")
		os.Exit(-1)
	}

	dstPath := dstFilename(opts.write, srcPath, opts.zipalgo)
	if opts.useDevNull {
		dstPath = os.DevNull
	}

	if opts.output != "" {
		dstPath = opts.output
	}

	dst := openDst(dstPath, opts.forceDstOverwrite)
	defer dst.Close()

	var cipher uint16 = aeadCipherAES
	if opts.encalgo == "chacha" {
		cipher = aeadCipherChaCha
	}

	if opts.encalgo == "aes" {
		cipher = aeadCipherAES
	}

	if opts.encalgo != "aes" && opts.encalgo != "chacha" && opts.encalgo != "none" {
		opts.encalgo = "none"
	}

	key := make([]byte, 32)

	if opts.keyderiv == "scrypt" {
		fmt.Printf("%s\n", "Using scrypt key derivation.")
		key = derivateAesKey([]byte("defaultpassword"), nil, 32)
		if key == nil {
			die(err)
		}
	}

	if opts.keyderiv == "random" {
		fmt.Printf("%s\n", "Using random key derivation.")
		if _, err := io.ReadFull(rand.Reader, key); err != nil {
			die(err)
		}
	}

	// Writing
	if opts.write {
		ew := io.WriteCloser(dst)
		// Encryption is enabled
		if opts.encalgo != "none" {
			ew, err = encrypt.NewWriterWithTypeAndBlockSize(dst, key, cipher, opts.maxblocksize)
			if err != nil {
				die(err)
			}
		}
		zw, err := compress.NewWriter(ew, algo)
		if err != nil {
			die(err)
		}
		_, err = io.Copy(zw, src)
		if err != nil {
			die(err)
		}
		if err := zw.Close(); err != nil {
			die(err)
		}
		if err := ew.Close(); err != nil {
			die(err)
		}
	}
	// Reading
	if opts.read {
		var reader io.ReadSeeker = src
		// Decryption is enabled
		if opts.encalgo != "none" {
			er, err := encrypt.NewReader(src, key)
			if err != nil {
				die(err)
			}
			reader = er
		}
		zr := compress.NewReader(reader)
		_, err = io.Copy(dst, zr)
		if err != nil {
			die(err)
		}
	}
}
~~~
~~~python
#!/usr/bin/env python
# encoding: utf-8

import sys
import json
import time
import timeit
import getpass
import subprocess
from statistics import mean

BINARY="./data/main"

def get_write_dummy(filesize):
    return "./data/movie_{0}".format(filesize)

def get_read_dummy(filesize):
    return "./movie_{0}".format(filesize)

def get_blocksizes(filesize):
    return [64 * 1024]
    #return [(2**x) for x in range(30) if 2**x >= 64 and (2**x)/1024**2 <= filesize]

def benchmark_preprocessing(config):
    print(config)
    if config["type"] == "write":
        path = get_write_dummy(config["filesize"])

    if config["type"] == "read":
        path = get_read_dummy(config["filesize"])

    for cmd in [
        "mkdir -p data",
        "sudo mount -t ramfs -o size=2G ramfs data",
        "sudo chmod 0777 data",
        "sudo dd if=/dev/urandom of={0} bs=1M count={1} conv=sync".format(path, config["filesize"]),
        "sudo chown -R {user}:users data".format(user=getpass.getuser()),
        "go build main.go",
        "cp ./main ./data/main"
    ]:
        print(cmd)
        if subprocess.call(cmd.split(), shell=False) != 0:
            return -1, "Error occured during setup of read benchmark."

    return 0, ""

def teardown(data):
    cmds = ["sudo umount -l data", "sudo rm data -rv"]
    if data["type"] == "read":
        cmds += ["sudo rm {0}".format(get_read_dummy(data["filesize"]))]
    for cmd in cmds:
        if subprocess.call(cmd.split(), shell=False) != 0:
            print("Error occured during teardown.")
            sys.exit(-1)

def build_write_cmd(data, block):
    cmd = "{binary} -k {keyderiv} -w -b {block} -D -e {enc} -f {inputfile}".format(
            keyderiv=data["kgfunc"],
            binary=BINARY,
            block=block,
            enc=data["encryption"],
            inputfile=get_write_dummy(data["filesize"])
        )
    return cmd.split()

def build_read_cmd(data, block):
    cmd = "{binary} -k {keyderiv} -r -b {block} -D -e {enc} -f {inputfile}".format(
            keyderiv=data["kgfunc"],
            binary=BINARY,
            block=block,
            enc=data["encryption"],
            inputfile=get_write_dummy(data["filesize"])
        )
    return cmd.split()

def build_prepare_read_cmd(data, block):
    cmd = "{binary} -k {keyderiv} -w -b {block} -e {enc} -o {outputfile} -f {inputfile}".format(
            keyderiv=data["kgfunc"],
            binary=BINARY,
            block=block,
            enc=data["encryption"],
            inputfile=get_read_dummy(data["filesize"]),
	    outputfile=get_write_dummy(data["filesize"])
        )
    return cmd.split()

def write_bench_data(data):
    filename = "{sys}_{type}_{enc}_{zip}_{fs}_{kd}.json".format(
        sys=data["system"],
        type=data["type"],
        enc=data["encryption"],
        zip=data["compression"],
        fs=data["filesize"],
        kd=data["kgfunc"]
    ).replace(" ", "_").replace("(", "[").replace(")", "]")
    with open(filename, "w") as fd:
        print("Writing {0}".format(filename))
        fd.write(json.dumps(data))

def benchmark(data):
    print("** Running {0} bench using {1} runs. **".format(data["type"], data["runs"]))
    print("Parameters for this run: {0}.".format(data))

    if data["type"] != "read" and data["type"] != "write":
        return -1, "Preparing read cmd failed."

    for blocksize in get_blocksizes(data.get("filesize")):

        if data["type"] == "read":
            pre_cmd = build_prepare_read_cmd(data, blocksize)
            if subprocess.call(pre_cmd) != 0:
                return -1, "Preparing read cmd failed."

            plaincmd = build_read_cmd(data, blocksize)
            cmd = "subprocess.call({cmd})".format(
                cmd=plaincmd
            )
            print("BS: {0} \t CMD:{1} ".format(blocksize, plaincmd))
            run = timeit.timeit(cmd, number=data["runs"], setup="import subprocess")

        if data["type"] == "write":
            cmd = "subprocess.call({cmd})".format(
                cmd=build_write_cmd(data, blocksize)
            )
            print("{0} bytes blocksize run...".format(blocksize))
            run = timeit.timeit(cmd, number=data["runs"], setup="import subprocess")

        data["results"].append(round(run/data["runs"]*1000))

    data["result-max"] = max(data["results"])
    data["result-min"] = min(data["results"])
    data["result-avg"] = mean(data["results"])
    return 0, data

def initialize(algo, runs, filesize):
    run_data = []
    enc, title = config["algos"]
    if enc in ["aes", "chacha", "none"]:
        run_config = {
            "encryption": enc,
            "compression": "none",
            "title": title,
            "runs": runs,
            "results": [],
            "kgfunc": config["kgfunc"],
            "system": config["system"],
            "filesize": filesize,
            "type": config["type"]
        }
        run_data.append(run_config)
    return run_data

def run_benchmark(config, runs=5, filesize=128):
    bench_inputs = initialize(config, runs, filesize)
    for bench_input in bench_inputs:
        err, msg = benchmark_preprocessing(bench_input)
        if err != 0:
            print(msg)
            sys.exit(err)
        err, output = benchmark(bench_input)
        if err != 0:
            print(output)
            sys.exit(err)
        write_bench_data(output)
        teardown(bench_input)

if __name__ == '__main__':

    for fs in [1, 2, 4, 8, 16, 32, 64, 128]:
        runs = [("aes", "AES/GCM"), ("chacha", "ChaCha20/Poly1305")]
        kgfuncs = ["none", "scrypt", "random"]
        for run in runs:
            for kgfunc in kgfuncs:
                for type in ["write"]:
                    config = {
                        "algos": run,
                        "kgfunc": kgfunc,
                        "system" : sys.argv[1],
                        "type": type
                    }
                    run_benchmark(config, runs=10, filesize=fs)

~~~
~~~python
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

LEGEND_MAP_SCRYPT = {
    'random': 'Dev Random generated key',
    'none': 'Static key',
    'scrypt': 'Scrypt generated key'
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
        line_chart.add(LEGEND_MAP_SCRYPT[v], [round(x.pop()) for x in d1[v]])
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
~~~
