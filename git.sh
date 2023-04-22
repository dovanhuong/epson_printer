#!/bin/bash
git pull
git add .
git commit -m $1
git branch -M main
git remote add origin https://github.com/dovanhuong/epson_printer.git
git push -u origin main
echo "completed commit...\n"
