#!/bin/bash

instructions(){
	echo -e "\nPyScalar v.0.8\n\n\tUso: $0 [--web]\n"
}

gui() {
	echo "Starting Web HTML GUI..."
	python -m gui.main;
}

PYSCALAR_PATH=$(pwd)/src
PYTHONPATH=$PYTHONPATH:$PYSCALAR_PATH
cd $PYSCALAR_PATH

if [[ -z $1 ]]; then
	echo "Hit <SPACE> for GUI execution..."
	read -n 1 -t 1 k;
	if [[ "$k" != " " ]]; then
		python -m app.pyscalar;
	else
		gui;
	fi
else 
	if [[ "$1" == "--web" ]]; then
		gui;
	else
		instructions;
	fi
fi

# Bye!
exit 0