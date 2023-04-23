#!/bin/bash
cd epson_printer
USER_SHELL=$(getent passwd hung | cut -d : -f 7)
$USER_SHELL
./run.sh
