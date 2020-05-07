#!/bin/bash

[ -f /usr/local/bin/cc ] && sudo rm /usr/local/bin/cc;
sudo curl -sSL https://raw.githubusercontent.com/mstfydmr/cc/master/cc.py -o /usr/local/bin/cc && \
sudo chmod a+x /usr/local/bin/cc