# Anhang D: Destails zur CPU--Architektur {#sec:APP_CPUARCH}

**System 1:**

Das erste System (Entwicklersystem Herr Piechula) ist ein Notebook mit *Intel
i5*--Architektur und *AES--NI*--Befehlserweiterungssatz. Der folgende
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

Das zweite System (Entwicklersystem Herr Pahl) ist ein Desktopsystem mit *AMD
Phenom X4*--Architektur ohne *AES--NI*--Befehlserweiterungssatz. Der folgende
`lscpu`--Ausschnitt zeigt die genauen Spezifikationen der CPU.

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

Das erste »low--end«--System ist ein Netbook auf *Intel Atom*--Basis mit einer
*32-bit--CPU*. Der folgende `lscpu`--Ausschnitt zeigt die genauen
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

Das zweite »low--end«--System ist ein *Raspberry Pi Zero*. Dieser hat die gleiche CPU
wie die erste Version des *Raspberry Pi*, jedoch mit einer dynamisch erhöhten Frequenz.
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
