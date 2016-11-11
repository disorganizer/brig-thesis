#!/usr/bin/env python
# encoding: utf-8

import sys
import json
import time
import timeit
import getpass
import subprocess

FILESIZE = 128
BINARY="./data/main"
WRITE_INPUT="./data/movie_{0}".format(FILESIZE)
READ_INPUT="./movie_{0}".format(FILESIZE)

BLOCKSIZES = [(2**x) for x in range(30) if 2**x >= 64 and (2**x)/1024**2 <= FILESIZE]


COMPRESSION_ALGOS = ["none", "lz4", "snappy"]
ENCRYPTION_ALGOS = ["none", "aes", "chacha"]
RUNS=5

def setup_write_benchmark():
    setup(WRITE_INPUT)

def setup_read_benchmark():
    setup(READ_INPUT)

def setup(path):
    for cmd in [
        "mkdir -p data",
        "sudo mount -t ramfs -o size=2G ramfs data",
        "sudo chmod 0777 data",
        "sudo dd if=/dev/urandom of={0} bs=1M count={1} conv=sync".format(path, FILESIZE),
        "sudo chown -R {user}:users data".format(user=getpass.getuser()),
        "go build main.go",
        "cp ./main ./data/main"
    ]:
        if subprocess.call(cmd.split(), shell=False) != 0:
            print("Error occured during setup of read benchmark.")
            sys.exit(-1)


def teardown(cmds):
    for cmd in cmds:
        if subprocess.call(cmd.split(), shell=False) != 0:
            print("Error occured during teardown.")
            sys.exit(-1)

def teardown_read():
    teardown_write()
    teardown(["sudo rm {0}".format(READ_INPUT)])

def teardown_write():
    teardown(["sudo umount -l data", "sudo rm data -rv"])

def build_write_cmd(data, block):
    cmd = "{binary} -w -b {block} -D -e {enc} -f {inputfile}".format(
            binary=BINARY,
            block=block,
            enc=data["encryption"],
            inputfile=WRITE_INPUT
        )
    return cmd.split()

def build_read_cmd(data, block):
    cmd = "{binary} -r -b {block} -D -e {enc} -f {inputfile}".format(
            binary=BINARY,
            block=block,
            enc=data["encryption"],
            inputfile=WRITE_INPUT
        )
    return cmd.split()

def build_prepare_read_cmd(data, block):
    cmd = "{binary} -w -b {block} -e {enc} -o {outputfile} -f {inputfile}".format(
            binary=BINARY,
            block=block,
            enc=data["encryption"],
            inputfile=READ_INPUT,
	    outputfile=WRITE_INPUT
        )
    return cmd.split()

def write_bench_data(data):
    filename = "{sys}_{type}_{enc}_{zip}.json".format(
        sys=data["system"],
        type=data["type"],
        enc=data["encryption"],
        zip=data["compression"]
    )
    with open(filename, "w") as fd:
        print("Writing {0}".format(filename))
        fd.write(json.dumps(data))

def get_input_parameters(system, encryption, compression, title, runs):
    if encryption not in ENCRYPTION_ALGOS or compression not in COMPRESSION_ALGOS:
        print("Invalid compression/encryption algorithm.")
        return None

    return {
        "encryption": encryption,
        "compression": compression,
        "title": title,
        "runs": runs,
        "results": [],
        "system": system,
        "type": "unknown"
    }

def write_benchmark(system, encryption, compression, title, runs=10):
    data = get_input_parameters(system, encryption, compression, title, runs)
    if data is None:
        print("Something went wrong - no correct data template available.")
        sys.exit(-1)

    print("** Running bench using {0} runs. **".format(data["runs"]))

    print("Parameters for this run: {0}.".format(data))
    for blocksize in BLOCKSIZES:
        cmd = "subprocess.call({cmd})".format(
            cmd=build_write_cmd(data, blocksize)
        )
        print("{0} bytes blocksize run...".format(blocksize))
        run = timeit.timeit(cmd, number=data["runs"], setup="import subprocess")
        data["results"].append(round(run/data["runs"]*1000))

    data["type"] = "write"
    return data

def read_benchmark(system, encryption, compression, title, runs=10):
    data = get_input_parameters(system, encryption, compression, title, runs)
    if data is None:
        print("Something went wrong - no correct data template available.")
        sys.exit(-1)

    print("** Running bench using {0} runs. **".format(data["runs"]))

    print("Parameters for this run: {0}.".format(data))
    for blocksize in BLOCKSIZES:
        # Write encrypted file to ramfs
        pre_cmd = build_prepare_read_cmd(data, blocksize)
        if subprocess.call(pre_cmd) != 0:
            print("Preparing read cmd failed.")
            sys.exit(-1)

        plaincmd = build_read_cmd(data, blocksize)
        cmd = "subprocess.call({cmd})".format(
            cmd=plaincmd
        )
        print("BS: {0} \t CMD:{1} ".format(blocksize, plaincmd))
        run = timeit.timeit(cmd, number=data["runs"], setup="import subprocess")
        data["results"].append(round(run/data["runs"]*1000))

    data["type"] = "read"
    return data

# Benchmark entry point
def run_read_bench(runs, system="unknown"):
    try:
        for enc, title in runs:
            data = read_benchmark(system=system, encryption=enc, compression="none" ,title=title, runs=RUNS)
            write_bench_data(data)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        teardown_read()

def run_write_bench(runs, system="unknown"):
    try:
        for enc, title in runs:
            data = write_benchmark(system=system, encryption=enc, compression="none", title=title, runs=RUNS)
            write_bench_data(data)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        teardown_write()

if __name__ == '__main__':

    if len(sys.argv) == 2:
        system = sys.argv[1]

    runs = [("aes", "AES/GCM"), ("none", "Base"), ("chacha", "ChaCha20/Poly1305")]

    setup_read_benchmark()
    run_read_bench(runs, system)

    setup_write_benchmark()
    run_write_bench(runs, system)
