#!/bin/bash

# kill all terminals, except the one this is running
kill $(pgrep bash)

activate_venv() {
	source venv/bin/activate
}

export -f activate_venv

VENV=""

if [ $# -eq 0 ]
then
    echo $'Running without Python Virtual Environment...\n'
else
	if [ $1 = 'venv' ]
	then
		VENV="activate_venv;"
		activate_venv
	fi
fi

gnome-terminal --tab -- bash -c "${VENV}pip3 -V; python3 server.py"
gnome-terminal --tab -- bash -c "${VENV}pip3 -V; python3 viewer.py"

pip3 -V
python3 student.py