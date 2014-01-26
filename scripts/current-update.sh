#!/bin/bash
eval `keychain --noask --eval id_dsa`  || exit 1
# get latest merge.py and friends
git pull || exit 1
./merge.py /var/git/ports-2013 || exit 1
