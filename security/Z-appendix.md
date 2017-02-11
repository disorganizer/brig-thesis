\appendix

# Anhang A: Umfang IPFS--Codebasis {#sec:APP_IPFS_LOC }

Nach einem frischen `git clone` vom IPFS--Repository wurde der Umfang des
Projekts ermittelt indem alle Abhängigkeiten mit `x install --global=false`
beschafft wurden. Im Anschluss wurden alle erkenntlichen
Drittanbieter--Bibliotheken in ein separates 3rd--Verzeichnis verschoben. Für
die Analyse wurde das Werkzeug `cloc`[^cloc] verwendet. Bei Analyse wurden die
autogenerieren Quelltextdateien (Protobuf, Endung »pb.go«) ausgeschlossen.
Die Analyse wurde auf die in der Programmiersprache Go geschriebenen Teile
begrenzt.

[^cloc]: GitHub--Seite des Projektes: <https://github.com/AlDanial/cloc>

Umfang IPFS--Projekt:

~~~sh

freya :: src/github.com/ipfs » cloc $(find ./go-ipfs -iname '*.go' -type f | \
                               grep -v 'pb.go')
     858 text files.
     844 unique files.
      14 files ignored.

github.com/AlDanial/cloc v 1.70  T=0.82 s (1026.5 files/s, 155950.9 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Go                             844          19983          10605          97639
-------------------------------------------------------------------------------
SUM:                           844          19983          10605          97639
-------------------------------------------------------------------------------
~~~

Umfang vom IPFS--Projekt genutzter Drittanbieter--Bibliotheken:

~~~sh
freya :: src/github.com/ipfs » cloc $(find ./3rd -iname '*.go' -type f | \
                               grep -v 'pb.go')
    1975 text files.
    1742 unique files.
     233 files ignored.

github.com/AlDanial/cloc v 1.70  T=6.02 s (289.3 files/s, 157793.5 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Go                            1742          57033          70893         822177
-------------------------------------------------------------------------------
SUM:                          1742          57033          70893         822177
-------------------------------------------------------------------------------
~~~

# Anhang B: IPFS--Grundlagen {#sec:APP_IPFS_SECWARNING}

Die Initialisierung als IPFS--Einstiegspunkt (gekürzt):

~~~sh
freya :: ~ » ipfs cat /ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme
Hello and Welcome to IPFS!

[...]

If you\'re seeing this, you have successfully installed
IPFS and are now interfacing with the ipfs merkledag!

 -------------------------------------------------------
| Warning:                                              |
|   This is alpha software. Use at your own discretion! |
|   Much is missing or lacking polish. There are bugs.  |
|   Not yet secure. Read the security notes for more.   |
 -------------------------------------------------------

Check out some of the other files in this directory:

  ./about
  ./help
  ./quick-start     <-- usage examples
  ./readme          <-- this file
  ./security-notes

~~~

Sicherheitshinweis von IPFS:

~~~sh
freya :: ~ » ipfs cat /ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/security-notes
                    IPFS Alpha Security Notes

We try hard to ensure our system is safe and robust, but all software
has bugs, especially new software. This distribution is meant to be an
alpha preview, don\'t use it for anything mission critical.

Please note the following:

- This is alpha software and has not been audited. It is our goal
  to conduct a proper security audit once we close in on a 1.0 release.

- ipfs is a networked program, and may have serious undiscovered
  vulnerabilities. It is written in Go, and we do not execute any
  user provided data. But please point any problems out to us in a
  github issue, or email security@ipfs.io privately.

- ipfs uses encryption for all communication, but it\'s NOT PROVEN SECURE
  YET!  It may be totally broken. For now, the code is included to make
  sure we benchmark our operations with encryption in mind. In the future,
  there will be an "unsafe" mode for high performance intranet apps.
  If this is a blocking feature for you, please contact us.
~~~

# Anfang C: IRC--Log zur TLS--Verschlüsselung {#sec:APP_IPFS_TRANSPORT_SEC}

IPFS--Entwickler:

* https://github.com/whyrusleeping
* https://github.com/Kubuxu

Brig--Entickler:

* manny (Christoph Piechula)

IRC--Logauszug vom 14.10.2016

~~~
(17:06:38) manny: Hi, is ipfs using currently any encryption (like TLS) for data
           tansport? Is there a spec?
(17:08:15) Kubuxu: yes, we are using minimalistic subset of TLS, secio
(17:10:27) manny: is there a spec online?
(17:11:22) manny: secio?
(17:11:24) whyrusleeping: manny: theres not a spec yet
(17:11:27) whyrusleeping: the code is here: https://github.com/libp2p/go-libp2p-secio
(17:11:33) manny: thx
(17:11:52) whyrusleeping: its not a '1.0' type release, we're still going to be
           changing a couple things moving forward
(17:12:04) whyrusleeping: and probably just straight up replace it with tls 1.3
           once its more common
(17:13:55) manny: As i never heard of secio, is it a known standard protocol - or
           something 'homemade'?
(17:16:27) Kubuxu: it is based of one of the modes of TLS 1.2 but it is homemade
(17:17:10) Kubuxu: it is based off one of TLS1.2 modes of operation but it is
           "homemade", that was the best option at the time
(17:18:00) Kubuxu: we plan to move to TLS1.3 when it is available
~~~

# Anhang D: Details zur CPU--Architektur {#sec:APP_CPUARCH}

**System 1:**

Das erste System (Entwicklersystem Herr Piechula) ist ein Notebook mit
Intel--i5--Architektur und AES--NI--Befehlserweiterungssatz. Der folgende
`lscpu`--Ausschnitt zeigt die genauen Spezifikationen der CPU.

~~~sh
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                4
On-line CPU(s) list:   0-3
Thread(s) per core:    2
Core(s) per socket:    2
Socket(s):             1
NUMA node(s):          1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 58
Model name:            Intel(R) Core(TM) i5-3320M CPU @ 2.60GHz
Stepping:              9
CPU MHz:               1460.278
CPU max MHz:           3300.0000
CPU min MHz:           1200.0000
BogoMIPS:              5190.46
Virtualization:        VT-x
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              3072K
NUMA node0 CPU(s):     0-3
Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca
cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx
rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology
nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est
tm2 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer
aes xsave avx f16c rdrand lahf_lm epb tpr_shadow vnmi flexpriority ept vpid
fsgsbase smep erms xsaveopt dtherm ida arat pln pts
~~~

**System 2:**

Das zweite System (Entwicklersystem Herr Pahl) ist ein Desktopsystem mit
AMD--Phenom--X4--Architektur ohne AES--NI--Befehlserweiterungssatz. Der
folgende `lscpu`--Ausschnitt zeigt die genauen Spezifikationen der CPU.

~~~sh

Architektur:           x86_64
CPU Operationsmodus:   32-bit, 64-bit
Byte-Reihenfolge:      Little Endian
CPU(s):                4
Liste der Online-CPU(s):0-3
Thread(s) pro Kern:    1
Kern(e) pro Socket:    4
Sockel:                1
NUMA-Knoten:           1
Anbieterkennung:       AuthenticAMD
Prozessorfamilie:      16
Modell:                4
Modellname:            AMD Phenom(tm) II X4 955 Processor
Stepping:              2
CPU MHz:               2100.000
Maximale Taktfrequenz der CPU:3200,0000
Minimale Taktfrequenz der CPU:800,0000
BogoMIPS:              6432.74
Virtualisierung:       AMD-V
L1d Cache:             64K
L1i Cache:             64K
L2 Cache:              512K
L3 Cache:              6144K
NUMA-Knoten0 CPU(s):   0-3
Markierungen:          fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca
cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb
rdtscp lm 3dnowext 3dnow constant_tsc rep_good nopl nonstop_tsc extd_apicid
eagerfpu pni monitor cx16 popcnt lahf_lm cmp_legacy svm extapic cr8_legacy abm
sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt nodeid_msr hw_pstate
vmmcall npt lbrv svm_lock nrip_save
~~~

**System 3:**

Das erste »low--end«--System ist ein Netbook auf Intel--Atom--Basis mit einer
32--bit--CPU. Der folgende `lscpu`--Ausschnitt zeigt die genauen
Spezifikationen der CPU.

~~~sh
Architecture:          i686
CPU op-mode(s):        32-bit
Byte Order:            Little Endian
CPU(s):                2
On-line CPU(s) list:   0,1
Thread(s) per core:    2
Core(s) per socket:    1
Socket(s):             1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 28
Model name:            Intel(R) Atom(TM) CPU N270   @ 1.60GHz
Stepping:              2
CPU MHz:               1600.000
CPU max MHz:           1600.0000
CPU min MHz:           800.0000
BogoMIPS:              3193.82
Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca
cmov pat clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe nx constant_tsc
arch_perfmon pebs bts aperfmperf pni dtes64 monitor ds_cpl est tm2 ssse3 xtpr
pdcm movbe lahf_lm dtherm
~~~

**System 4:**

Das zweite »low--end«--System ist ein Raspberry Pi Zero. Dieser hat die gleiche CPU
wie die erste Version des Raspberry Pi, jedoch mit einer dynamisch erhöhten Frequenz.
Der folgende `lscpu`--Ausschnitt zeigt die genauen Spezifikationen der CPU.

~~~sh
Architecture:          armv6l
Byte Order:            Little Endian
CPU(s):                1
On-line CPU(s) list:   0
Thread(s) per core:    1
Core(s) per socket:    1
Socket(s):             1
Model name:            ARMv6-compatible processor rev 7 (v6l)
CPU max MHz:           1000.0000
CPU min MHz:           700.0000
Linux luna 4.4.30-1-ARCH #1 Tue Nov 1 21:44:33 MDT 2016 armv6l GNU/Linux
~~~

# Anhang E: Benchmark--Skripte {#sec:APP_SCRIPTE}

Bash--Skript zur Ermittlung der Lese-- und Schreibgeschwindigkeit mittels `dd`:

~~~sh
#/bin/sh

BENCHDIR=thisfoldershouldnotexist
TESTFILE=thisfileshouldnotexist

READACC=0
WRITEACC=0

function read_bench() {
	sudo echo 3 > /proc/sys/vm/drop_caches
	RESULT=`dd if=/boot/$TESTFILE of="$BENCHDIR/$TESTFILE" bs=1M count=256 oflag=sync 2>&1 | tail -n 1| awk '{ gsub(",","."); print $(NF-1) }'`
	READACC=`python3 -c "print($READACC+$RESULT)"`
}

function write_bench() {
	sudo echo 3 > /proc/sys/vm/drop_caches
	RESULT=`dd if=$BENCHDIR/$TESTFILE of=/boot/$TESTFILE bs=1M count=256 oflag=sync 2>&1 | tail -n 1| awk '{ gsub(",","."); print $(NF-1) }'`
	WRITEACC=`python3 -c "print($WRITEACC+$RESULT)"`
}


echo "Mounting benchmark dir..."
sudo swapoff -a
mkdir -p $BENCHDIR
sudo mount -t ramfs -o size=260M ramfs $BENCHDIR
sudo chmod 0777 $BENCHDIR
sudo dd if=/dev/urandom of=/boot/$TESTFILE bs=1M count=256 oflag=sync

echo "Running read benchmark..."
for i in `seq 1 10`;
do
	read_bench
done
echo Read performance: `python3 -c "print($READACC/10)"`

echo "Running write benchmark..."
for i in `seq 1 10`;
do
	write_bench
done
echo Write performance: `python3 -c "print($WRITEACC/10)"`

sudo sync
sudo swapon -a
echo "Cleaning up..."
sudo umount $BENCHDIR
rmdir $BENCHDIR
sudo rm /boot/$TESTFILE
~~~

Kommandozeilen--Tool für Ver-- und Entschlüsselung:

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

Python Skript für die Erhebung der Benchmark--Daten im Hilfe des
Kommandozeilen--Tools zur Ver-- und Entschlüsselung von Dateien:

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

Python Skript für das Plotten der Benchmark--Daten:

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
    input_data["outputfile"] = os.path.join(
	    dir_path, os.path.basename(config_path) + ".svg"
	)

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
        [
			"inkscape",
			"{0}".format(input_data["outputfile"]),
			"--export-pdf={0}.pdf".format(input_data["outputfile"])
		]
    )
    subprocess.call(
        ["chromium", "{0}".format(input_data["outputfile"]), "&"]
    )
~~~

# Schlüsselgenerierung auf der Smartcard {#sec:APP_SCHLUESSELGENERIERUNG_AUF_DER_KARTE}

~~~sh
gpg/card> admin
Admin commands are allowed

gpg/card> generate
Make off-card backup of encryption key? (Y/n) Y
gpg: error checking the PIN: Card error

gpg/card> generate
Make off-card backup of encryption key? (Y/n) Y
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 5y
Key expires at Fr 10 Dez 2021 13:44:18 CET
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: Christoph Piechula
Email address: christoph@nullcat.de
Comment:
You selected this USER-ID:
    "Christoph Piechula <christoph@nullcat.de>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: Note: backup of card key saved to '/home/qitta/.gnupg/sk_E5A1965037A8E37C.gpg'
gpg: key 932AEBFDD72FE59C marked as ultimately trusted
gpg: revocation certificate stored as '/home/qitta/.gnupg/openpgp-revocs.d/D61CEE19369B9C330A4A482D932AEBFDD72FE59C.rev'
public and secret key created and signed.
~~~

Generierte Schlüssel Anzeigen lassen

~~~sh
gpg/card> list

Reader ...........: 0000:0000:X:0
Application ID ...: 00000000000000000000000000000000
Version ..........: 2.0
Manufacturer .....: Yubico
Serial number ....: 00000000
Name of cardholder: Christoph Piechula
Language prefs ...: [not set]
Sex ..............: male
URL of public key : [not set]
Login data .......: [not set]
Signature PIN ....: forced
Key attributes ...: rsa2048 rsa2048 rsa2048
Max. PIN lengths .: 127 127 127
PIN retry counter : 3 3 3
Signature counter : 4
Signature key ....: D61C EE19 369B 9C33 0A4A  482D 932A EBFD D72F E59C
      created ....: 2016-12-11 12:44:36
Encryption key....: DD5E 14EE D04D 58AB 85D7  0AB3 E5A1 9650 37A8 E37C
      created ....: 2016-12-11 12:44:36
Authentication key: 4E45 FC88 A1B1 292F 6CFA  B577 4CE8 E35B 8002 9F6E
      created ....: 2016-12-11 12:44:36
General key info..: pub  rsa2048/932AEBFDD72FE59C 2016-12-11 Christoph Piechula <christoph@nullcat.de>
sec>  rsa2048/932AEBFDD72FE59C  created: 2016-12-11  expires: 2021-12-10
                                card-no: 0006 00000000
ssb>  rsa2048/4CE8E35B80029F6E  created: 2016-12-11  expires: 2021-12-10
                                card-no: 0006 00000000
ssb>  rsa2048/E5A1965037A8E37C  created: 2016-12-11  expires: 2021-12-10
                                card-no: 0006 00000000

gpg/card>
~~~

Schlüssel mit GnuPG anzeigen lassen:

~~~sh
freya :: code/brig-thesis/security ‹master*› » gpg --list-keys 932AEBFDD72FE59C
pub   rsa2048 2016-12-11 [SC] [expires: 2021-12-10]
      D61CEE19369B9C330A4A482D932AEBFDD72FE59C
uid           [ultimate] Christoph Piechula <christoph@nullcat.de>
sub   rsa2048 2016-12-11 [A] [expires: 2021-12-10]
sub   rsa2048 2016-12-11 [E] [expires: 2021-12-10]

freya :: code/brig-thesis/security ‹master*› » gpg --list-secret-keys 932AEBFDD72FE59C
sec>  rsa2048 2016-12-11 [SC] [expires: 2021-12-10]
      D61CEE19369B9C330A4A482D932AEBFDD72FE59C
      Card serial no. = 0006 00000000
uid           [ultimate] Christoph Piechula <christoph@nullcat.de>
ssb>  rsa2048 2016-12-11 [A] [expires: 2021-12-10]
ssb>  rsa2048 2016-12-11 [E] [expires: 2021-12-10]
~~~

# Unterschlüssel erstellen {#sec:APP_UNTERSCHLUESSEL_ERSTELLEN}

~~~sh
$ gpg --expert --edit-key E9CD5AB4075551F6F1D6AE918219B30B103FB091
gpg (GnuPG) 2.1.16; Copyright (C) 2016 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2017-01-31  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2017-01-31  usage: E
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
Your selection? 4
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048)
Requested keysize is 2048 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years

Key is valid for? (0) 2y
Key expires at Di 11 Dez 2018 17:33:54 CET
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2017-01-31  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2017-01-31  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
Your selection? 8

Possible actions for a RSA key: Sign Encrypt Authenticate
Current allowed actions: Sign Encrypt

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? e

Possible actions for a RSA key: Sign Encrypt Authenticate
Current allowed actions: Sign

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? s

Possible actions for a RSA key: Sign Encrypt Authenticate
Current allowed actions:

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? a

Possible actions for a RSA key: Sign Encrypt Authenticate
Current allowed actions: Authenticate

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? q
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048)
Requested keysize is 2048 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 2y
Key expires at Di 11 Dez 2018 17:35:18 CET
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2017-01-31  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2017-01-31  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> save

~~~

# Ablaufdatum ändern {#sec:APP_ABLAUFDATUM_AENDERN}

Ablaufdatum für den Hauptschlüssel und für den Unterschlüssel zum
Ver--/Entschlüsseln ändern:

~~~sh
$ gpg --expert --edit-key E9CD5AB4075551F6F1D6AE918219B30B103FB091
gpg (GnuPG) 2.1.16; Copyright (C) 2016 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2017-01-31  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2017-01-31  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> expire
Changing expiration time for the primary key.
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 10y
Key expires at Mi 09 Dez 2026 17:45:52 CET
Is this correct? (y/N) y

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2017-01-31  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> key 1

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb* rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2017-01-31  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> expire
Changing expiration time for a subkey.
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 2y
Key expires at Di 11 Dez 2018 17:46:03 CET
Is this correct? (y/N) y

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb* rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> save
~~~

# Exportieren der GnuPG--Schlüssel {#sec:APP_EXPORTIEREN_DER_PRIVATEN_UND_OEFFENTLICHEN_SCHLUESSEL}

Exportieren der privaten Schlüssel:

~~~sh
$ gpg --armor --export E9CD5AB4075551F6F1D6AE918219B30B103FB091 \
  > E9CD5AB4075551F6F1D6AE918219B30B103FB091.pub
$ gpg --armor --export-secret-keys \
  > E9CD5AB4075551F6F1D6AE918219B30B103FB091.sec
$ gpg --armor --export-secret-subkeys \
  > E9CD5AB4075551F6F1D6AE918219B30B103FB091.secsub
~~~

# Schlüssel auf die Smartcard verschieben {#sec:APP_SCHLUESSEL_AUF_SMARTCARD_VERSCHIEBEN}

~~~sh
$ gpg --expert --edit-key E9CD5AB4075551F6F1D6AE918219B30B103FB091
gpg (GnuPG) 2.1.16; Copyright (C) 2016 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> key 1

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb* rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> keytocard
Please select where to store the key:
   (2) Encryption key
Your selection? 2

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb* rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> key 2

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb* rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb* rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> keytocard
You must select exactly one key.

gpg> key 1

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb* rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> keytocard
Please select where to store the key:
   (1) Signature key
   (3) Authentication key
Your selection? 1

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb* rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> key 2

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb  rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> key 3

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb* rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> keytocard
Please select where to store the key:
   (3) Authentication key
Your selection? 3

sec  rsa2048/8219B30B103FB091
     created: 2013-02-09  expires: 2026-12-09  usage: SC
     trust: ultimate      validity: ultimate
ssb  rsa2048/0B81E5BF85821570
     created: 2013-02-09  expires: 2018-12-11  usage: E
ssb  rsa2048/2CC4F84BE43F54ED
     created: 2016-12-11  expires: 2018-12-11  usage: S
ssb* rsa2048/74B050CC5ED64D18
     created: 2016-12-11  expires: 2018-12-11  usage: A
[ultimate] (1). Christoph Piechula <christoph@nullcat.de>

gpg> save
~~~

# User-- und Admin--PIN ändern {#sec:APP_USER_UND_ADMIN_PIN_AENDERN}

~~~sh
freya :: code/brig-thesis/security ‹master*› » gpg --card-edit

Reader ...........: 0000:0000:X:0
Application ID ...: 00000000000000000000000000000000
Version ..........: 2.0
Manufacturer .....: Yubico
Serial number ....: 00000000
Name of cardholder: [not set]
Language prefs ...: [not set]
Sex ..............: unspecified
URL of public key : [not set]
Login data .......: [not set]
Signature PIN ....: forced
Key attributes ...: rsa2048 rsa2048 rsa2048
Max. PIN lengths .: 127 127 127
PIN retry counter : 3 3 3
Signature counter : 1
Signature key ....: 7CD8 DB88 FBF8 22E1 3005  66D1 2CC4 F84B E43F 54ED
      created ....: 2016-12-11 16:32:58
Encryption key....: 6258 6E4C D843 F566 0488  0EB0 0B81 E5BF 8582 1570
      created ....: 2013-02-09 23:18:50
Authentication key: 2BC3 8804 4699 B83F DEA0  A323 74B0 50CC 5ED6 4D18
      created ....: 2016-12-11 16:34:21
General key info..: sub  rsa2048/2CC4F84BE43F54ED 2016-12-11 Christoph Piechula <christoph@nullcat.de>
sec   rsa2048/8219B30B103FB091  created: 2013-02-09  expires: 2026-12-09
ssb>  rsa2048/0B81E5BF85821570  created: 2013-02-09  expires: 2018-12-11
                                card-no: 0006 00000000
ssb>  rsa2048/2CC4F84BE43F54ED  created: 2016-12-11  expires: 2018-12-11
                                card-no: 0006 00000000
ssb>  rsa2048/74B050CC5ED64D18  created: 2016-12-11  expires: 2018-12-11
                                card-no: 0006 00000000

gpg/card> admin
Admin commands are allowed

gpg/card> passwd
gpg: OpenPGP card no. 00000000000000000000000000000000 detected

1 - change PIN
2 - unblock PIN
3 - change Admin PIN
4 - set the Reset Code
Q - quit

Your selection? 1
PIN changed.

1 - change PIN
2 - unblock PIN
3 - change Admin PIN
4 - set the Reset Code
Q - quit

Your selection? 3
PIN changed.

1 - change PIN
2 - unblock PIN
3 - change Admin PIN
4 - set the Reset Code
Q - quit

Your selection? Q

gpg/card> quit
~~~

# YubiCloud Zwei--Faktor--Authentifizierung {#sec:APP_YUBICLOUD_AUTHENTIFIZIERUNG}

Das folgende Code--Snippet zeigt nur eine vereinfachte
Proof--of--Concept--Implementierung. Im Produktiv--Code müssten beispielsweise
Daten wie Passwort und YubikeyID mittels einer Passwortableitungsfunktion
verwaltet werden.

~~~go
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/GeertJohan/yubigo"
	"github.com/fatih/color"
)

const (
	RegistredYubikeyID = "ccccccelefli"
	UserPassword       = "katzenbaum"
)

func boolToAnswer(answer bool) string {
	if answer {
		return color.GreenString("OK")
	}
	return color.RedString("X")
}

func main() {
	password, otp := os.Args[1], os.Args[2]
	yubiAuth, err := yubigo.NewYubiAuth("00000", "000000000000000000000000000=")

	if err != nil {
		log.Fatalln(err)
	}

	// Validierung an der Yubico Cloud
	_, ok, err := yubiAuth.Verify(otp)
	if err != nil {
		log.Println(err)
	}

	fmt.Printf("[yubico: %s, ", boolToAnswer(ok))
	fmt.Printf("brig : %s, ", boolToAnswer(otp[0:12] == RegistredYubikeyID))
	fmt.Printf("password: %s]\n", boolToAnswer(password == UserPassword))
}
~~~

\newpage

\let\oldhypertarget\hypertarget

\renewcommand{\hypertarget}[2]{%
    \leavevmode%
    \oldhypertarget{#1}{#2}%
}

\clearpairofpagestyles
\ihead{}
\ohead{Literaturverzeichnis}

# Literaturverzeichnis
