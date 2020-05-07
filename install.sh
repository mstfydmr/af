#!/bin/bash

pip3 install python-gitlab  || pip install python-gitlab
pip3 install python-slugify || pip install python-slugify

[ -f /usr/local/bin/af ] && sudo rm /usr/local/bin/af;
sudo curl -sSL https://raw.githubusercontent.com/mstfydmr/af/master/af.py -o /usr/local/bin/af && \
sudo chmod a+x /usr/local/bin/af