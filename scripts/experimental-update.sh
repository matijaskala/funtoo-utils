#!/bin/bash
eval `keychain --noask --eval id_dsa`  || exit 1
# get latest merge.py and friends
git pull || exit 1
./merge.py --branch experimental /var/git/experimental-mini-2011 || exit 1
