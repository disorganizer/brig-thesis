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
