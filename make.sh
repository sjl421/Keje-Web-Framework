#!/bin/bash
# This scripts will do move the files to python dist-packages
# Run this file via sudo
if [ "$(uname)" == "Darwin" ]; then # if its mac
    DEST_PATH='/usr/lib/python2.7/dist-packages' # python dist-packages path   
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    DEST_PATH='/usr/lib/python2.7/dist-packages' # python dist-packages path
fi
mkdir "$DEST_PATH/Keje"
cp __init__.py server.py keje.py request_handler.py "$DEST_PATH"/Keje