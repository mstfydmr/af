#!/bin/bash

[ -f /usr/local/bin/af ] && sudo rm /usr/local/bin/af;
sudo curl -sSL https://raw.githubusercontent.com/mstfydmr/af/master/af.py -o /usr/local/bin/af && \
sudo chmod a+x /usr/local/bin/af