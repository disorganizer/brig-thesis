#!/bin/sh

rm data/ipfs -rf
export IPFS_PATH=./data/ipfs
export BRIG_PATH=./data/brig
ipfs init


function time_it() {
	ts=$(date +%s%N)
	$*
	tt=$((($(date +%s%N) - $ts)/1000000))
	>&2 echo "Time taken: $tt"

}

function create_ramfs() {
	mkdir -p data
	sudo mount -t ramfs -o size=2G ramfs data
	sudo chmod 0777 data
	sudo chown -R sahib:users data
}

function copy_sized() {
	echo "Copying $3 MB of $1 to $2"
	dd if="$1" of="$2" bs=1M count="$3" status=none
}

##### write functions:

function compress_to_ipfs() {
	./main -f -a $2 $3 -s -c $1 | ipfs add -q > /dev/null
}

function compress_single() {
	./main -f -D -a $2 $3 -c $1
}

function add_to_ipfs() {
	ipfs add -q $1
}

function baseline_write() {
	time_it cat $1 > /dev/null
}

##### read functions:

function compress_to_ipfs_and_read() {
	HASH=$(./main -f -a $2 $3 -s -c $1 | ipfs add -q)
	ipfs cat $HASH | time_it ./main -f -a $2 $3 -d $1.$2
}

function compress_single_and_read() {
	./main -f -a $2 $3 -c $1
	time_it ./main -f -a $2 $3 -d $1.$2
}

function add_to_ipfs_and_read() {
	HASH=`ipfs add -q $1`
	time_it ipfs cat $HASH > /dev/null
}

function baseline_read() {
	time_it dd if=$1 of=/dev/null bs=4M status=none
}

# Init:
create_ramfs
size=1
for i in `seq 10`; do
	copy_sized "input/movie.mp4" "data/movie_$size" $size
	copy_sized "input/archive.tar" "data/archive_$size" $size
	size=$(expr $size \* 2)
done

function sample() {
	echo "=== $*"
	local size=1
	for i in `seq 10`; do
		$1 "data/archive_$size" $2 $3 $4 $5 $6
		size=$(expr $size \* 2)
	done

	rm data/*.$2 -f
}

sample baseline_read
sample add_to_ipfs
sample compress_single_and_read snappy
sample compress_single_and_read none -e
sample compress_single_and_read snappy -e
sample compress_to_ipfs snappy
sample compress_to_ipfs snappy -e

function create_brig_repo() {
	pkill -9 brig
	rm data/brig -rf
	brig -x ThiuJ9wesh --nodaemon init alice@jabber.nullcat.de/laptop
	brig -x ThiuJ9wesh daemon launch 2>/dev/null &
	echo "...waiting for daemon to catch up..."
	sleep 5
	fusermount -u data/mount
	mkdir -p data/mount
	brig mount data/mount
}


create_brig_repo
size=1
for i in `seq 10`; do
	time_it brig add "data/archive_$size"
	time_it brig cat "archive_$size" /dev/null
	time_it dd if="data/mount/archive_$size" of=/dev/null bs=4M status=none
	size=$(expr $size \* 2)
done
