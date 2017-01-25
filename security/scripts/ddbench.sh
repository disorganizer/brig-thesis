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
