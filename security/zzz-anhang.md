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

\newpage
# Literaturverzeichnis
