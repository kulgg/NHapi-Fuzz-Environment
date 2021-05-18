#!/bin/bash

maxcores=4
inpdir="Inputs/2"
outputdir="Findings"
maxmemory=10000
timeout=5000
executable="dotnet Harness/nHapi.Fuzz/bin/Debug/netcoreapp3.1/nHapi.Fuzz.dll"

afl-fuzz -i $inpdir -o $outputdir -m $maxmemory -t $timeout -M core0 $executable &
count=1
for ((i=1;i<=maxcores-2;i++))
do
	afl-fuzz -i $inpdir -o $outputdir -m $maxmemory -t $timeout -S core$i $executable &
	let "count++"
done
afl-fuzz -i $inpdir -o $outputdir -m $maxmemory -t $timeout -S core$count $executable