#!/bin/sh
#sudo apt-get install graphviz libgraphviz-dev graphviz-dev python-pygraphviz
git clone https://github.com/jjguy/heatmap.py.git
git clone https://github.com/wiredfool/Python-Imaging-Library-G4-Tiff-Support.git
cd heatmap.py
python setup.py install
cd ../Python-Imaging-Library-G4-Tiff-Support
python setup.py install