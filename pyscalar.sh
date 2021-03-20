#!/bin/bash

instructions(){
	echo -e "\nPyScalar v.0.9\n\n\tUso: $0 [--web]\n"
}

gui() {
	echo "Starting Web HTML GUI..."
	python3 -m gui.main;
}

PYSCALAR_PATH="$(pwd)/src"
PYTHONPATH="${PYTHONPATH}:${PYSCALAR_PATH}:${PYSCALAR_PATH}/gui"
cd "$PYSCALAR_PATH" || exit

if [[ -z $1 ]]; then
	echo "Hit <SPACE> for GUI execution..."
	read -r -n 1 -t 1 k;
	if [[ "$k" != " " ]]; then
		python3 -m app.pyscalar;
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