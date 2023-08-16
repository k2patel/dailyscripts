#!/bin/zsh

# Capture the output of the ioreg command and extract the PID
pids=($(ioreg -l -w 0 | grep -o '"kCGSSessionSecureInputPID"=[0-9]\+' | cut -d= -f2 | uniq))

for pid in "${pids[@]}"; do
    if [[ -n $pid ]]; then
        echo "Extracted PID: $pid"
        ps auxww | grep "\<$pid\>"
    else
        echo "PID not found in the input."
    fi
done
