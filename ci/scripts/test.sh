#!/bin/bash

set -e
SCRIPT_DIR=`pwd`/`dirname $0`
echo "Script Directory: $SCRIPT_DIR"

source $SCRIPT_DIR/common.sh

run_tests() {
    COMPONENT=$1
    echo "Testing in component: $COMPONENT"

    OLD_DIR=`pwd`

    cd $COMPONENT
    source $COMPONENT/$TEST_FILE

    cd $OLD_DIR

}

JOB_DIR=`pwd`
echo "Job Directory: $JOB_DIR"

SOURCE_DIR=$JOB_DIR/source
echo "SOURCE Directory: $SOURCE_DIR"

VENV_DIR=$JOB_DIR/venvs
echo "VENV Directory: $VENV_DIR"

poetry config virtualenvs.path ${VENV_DIR}

for COMPONENT in $(get_changed_components ./source/.git/resource/changed_files)
do  
    COMPONENT_DIR=$SOURCE_DIR/$COMPONENT

    echo "Checking component: $COMPONENT"
    echo "Component directory: $COMPONENT_DIR"

    if component_has_tests $COMPONENT_DIR;
    then
        run_tests $COMPONENT_DIR
    else
        echo "Component has no tests: $COMPONENT"
    fi
done
