#!/bin/bash

pip install -r requirements.txt

# Configuring fzf tool in your terminal -> Press ctrl + R in terminal,
# and enjoy pleasing commandhistory
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --all

