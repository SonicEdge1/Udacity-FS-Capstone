#!/bin/bash

must be in the /backend folder before running script
MY_PWD=$(pwd);
LAST_DIR=${MY_PWD##*/}
EXPECTED_DIR="backend"
if [[ {$LAST_DIR} = {$EXPECTED_DIR} ]]; then
    echo "Operating in expected directory: " $EXPECTED_DIR;
else
    echo "NOT in expected directory: " $EXPECTED_DIR "   exiting script... ";
    exit 1;
fi
source ./env/bin/activate
pip install -r requirements.txt

source ./setup.sh

flask run --reload
echo "done";
