#!/bin/bash

maxcores = 26
inpdir = "Inputs/2"
outputdir = "Findings"
maxmemory = 10000
timeout = 14000
executable = "dotnet nHapi.Fuzz/bin/Debug/netcoreapp3.1/nHapi.Fuzz.dll"

afl-fuzz -i $inpdir -o $outputdir -m $maxmemory -t $timeout -M core0 $executable &
for ((i=1;i<=maxcores;i++))
do
	afl-fuzz -i $inpdir -o $outputdir -m $maxmemory -t $timeout -S core$i $executable &
done
let "maxcores++"
afl-fuzz -i $inpdir -o $outputdir -m $maxmemory -t $timeout -S core$maxcores $executable