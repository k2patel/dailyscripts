#!/usr/bin/env bash

# Redirect log to logger
exec 1> >(logger -t $(basename $0)) 2>&1
 
# Going to the apache log folder
cd /var/log/apache2 || exit 1

# define search for last 7 day
lst=7

# loop for 7 day
while [ ${lst} -gt 0 ] 

do

        for i in  *.`date -d "-${lst} days" +%Y-%m-%e*`
        do 
            if [[ ${i} =~ \.log$ ]]; then
                echo "zipping log ${i}"
                /bin/gzip ${i}
            fi
        done
lst=$(( $lst - 1 ))
done
