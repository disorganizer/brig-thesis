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

\newpage
# Literaturverzeichnis
