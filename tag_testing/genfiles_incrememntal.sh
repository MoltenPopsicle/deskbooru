#!/bin/bash
count=1
times_run=1
files_no="$2"
dirs_no="$3"

if [ -n "$dirs_no" ]; then
    for i in $(seq 0 $dirs_no); do
        echo "$i"
        mkdir "$1"/size_"$i";
    done
fi


if [ -z $dirs_no ]; then
    dirs=$1
    count=$((1000000 / $2 ))
else
    dirs=$(ls $1 | sort -n)
fi

for i in $dirs; do
    echo "$i"
    echo "$dirs"
    echo "$1"
    echo "CURRENT COUNT IS $count; dd HAS BEEN RUN $times_run TIMES; NUMBER OF FILES TO BE MADE IS $files_no"
    for n in $(seq 1 $files_no); do
        if [ $i = $1 ]; then
            pv /dev/urandom | dd of=$1/_speedtest_$n bs=1024 count=$count;
        else
            echo "d"
            #pv /dev/urandom | dd of=$(pwd)/$1/$i/"$i"_speedtest_$n bs=1024 count=$count;
        fi
        done
	times_run=$(($times_run + 1))

    if (($files_no > 1)); then
		files_no=$(($files_no / 3))
	fi


    if (($times_run < 9)); then
		count=$(($count * 8))
	else
		count=$(($count * 3))
	fi;
done
