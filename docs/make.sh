#!/bin/sh

make clean
sphinx-apidoc -o source/code/ ..
make html

python3 -m http.server --directory build/html
