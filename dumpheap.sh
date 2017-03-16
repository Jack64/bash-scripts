#!/bin/bash
PID=$1
outfile="dump.bin"
heap_start=$(cat /proc/$PID/maps 2>/dev/null | grep heap | cut -d' ' -f1 | cut -d- -f1)
heap_end=$(cat /proc/$PID/maps 2>/dev/null | grep heap | cut -d' ' -f1 | cut -d- -f2)
if [ -z $heap_start ]
then
        echo "[-] Process not found"
        exit 1
else
        echo "[*] Dumping memory..."
        echo -en "attach $PID \n dump binary memory $outfile 0x$heap_start 0x$heap_end \n quit \n" | gdb >/dev/null 2>&1
        echo "[+] Heap dumped to $outfile"
fi

