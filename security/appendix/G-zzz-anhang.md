# *YubiCloud* Zwei--Faktor--Authentifizierung {#sec:APP_YUBICLOUD_AUTHENTIFIZIERUNG}

Das folgende Code--Snippet zeigt nur eine vereinfachte
Proof--of--Concept--Implementierung. Im Produktivcode müssten beispielsweise
Daten wie Passwort und YubikeyID mit mittels einer Passwortableitungfunktion
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
