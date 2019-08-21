# Random Scrips

1. gitsync:
    * this script syncronize the git repository including submodule ( wiping out local changes )

2. nexenta/list_folder_size
    * This script will list all the folder and sizes on nexenta share.

3. bash_profile ssh complition using alias
    ```bash
    alias c='/usr/bin/ssh'
    export HLIST
    HLIST=`cat ~/.ssh/known_hosts | cut -f 1 -d ' ' | sed -e s/,.*//g | uniq | grep -v "\["`
    HLIST="${HLIST} $(cat ~/.ssh/config | grep Host | awk '{print $2}' | grep -v \*)"
    HLIST=$(echo ${HLIST} | sort | uniq)
    complete -W "${HLIST}" c
    ```
