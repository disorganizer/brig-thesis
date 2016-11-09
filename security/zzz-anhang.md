# Anhang A: Umfang IPFS--Codebasis {#sec:APP_IPFS_LOC }

Nach einem frischen `git clone` vom *IPFS*--Repository wurde der Umfang des
Projekts ermittelt indem alle Abhängigkeiten mit `x install --global=false`
beschafft wurden. Im Anschluss wurden alle erkenntlichen
Drittanbieter--Bibliotheken in ein separates *3rd*--Verzeichnis verschoben. Für
die Analyse wurde das Werkzeug `cloc`[^cloc] verwendet. Bei Analyse wurden die
autogenerieren Quelltextdateien (*Protobuf*, Endung »pb.go«) ausgeschlossen.
Die Analyse wurde auf die in der Programmiersprache *Go* geschriebenen Teile
begrenzt.

[^cloc]: Github--Seite des Projektes: <https://github.com/AlDanial/cloc>

Umfang *IPFS*--Projekt:

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

Umfang vom *IPFS*--Projekt genutzter Drittanbieter--Bibliotheken:

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

# Anfang B: IPFS--Grundlagen {#sec:APP_IPFS_SECWARNING}

Die Initialisierung als *IPFS*--Einstiegspunkt (gekürzt):

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

Sicherheitshinweis von *IPFS*:

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

# Anfang C: IRC--Logauszug zur Transportverschlüsselung {#sec:APP_IPFS_TRANSPORT_SEC}

IPFS--Entwickler:

* https://github.com/whyrusleeping
* https://github.com/Kubuxu

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

# Anfang D: Destails zur CPU--Architektur {#sec:APP_CPUARCH}

**System 1:**
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

**System 2:**
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

\newpage
# Literaturverzeichnis
