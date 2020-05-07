#!/bin/bash

[ -f /usr/local/bin/cc ] && sudo rm /usr/local/bin/cc;
sudo curl -sSL https://raw.githubusercontent.com/criexe/dropbox-backup/master/main.sh -o /usr/local/bin/criexe-dropbox-backup && \
sudo chmod a+x /usr/local/bin/criexe-dropbox-backup