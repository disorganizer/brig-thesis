package main

import (
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
	forceDstOverwrite := flag.Bool("f", false, "Force overwriting destination file.")
	useDevNull := flag.Bool("D", false, "Write to /dev/null.")
	flag.Parse()
	return options{
		read:              *read,
		write:             *write,
		zipalgo:           *zipalgo,
		encalgo:           *encalgo,
		output:            *output,
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
	// key := derivateAesKey([]byte("defaultpassword"), nil, 32)
	//if key == nil {
	//	die(err)
	//}
	key := make([]byte, 32)
	if opts.encalgo == "chacha" {
		cipher = aeadCipherChaCha
	}

	if opts.encalgo == "aes" {
		cipher = aeadCipherAES
	}

	if opts.encalgo != "aes" && opts.encalgo != "chacha" && opts.encalgo != "none" {
		opts.encalgo = "none"
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
