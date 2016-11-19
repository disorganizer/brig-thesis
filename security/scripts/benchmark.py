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

