# Schlüsselgenerierung auf der Karte

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

~~~
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

# Schlüssel mit gpg anzeigen lassen

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

# Unterschlüssel erstellen

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

# Exportieren der privaten und öffentlichen Schlüssel

~~~sh
$ gpg --armor --export E9CD5AB4075551F6F1D6AE918219B30B103FB091 \
  > E9CD5AB4075551F6F1D6AE918219B30B103FB091.pub
$ gpg --armor --export-secret-keys \
  > E9CD5AB4075551F6F1D6AE918219B30B103FB091.sec
$ gpg --armor --export-secret-subkeys \
  > E9CD5AB4075551F6F1D6AE918219B30B103FB091.secsub
~~~

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

# pin change

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
~~~
