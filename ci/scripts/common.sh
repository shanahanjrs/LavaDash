#!/bin/bash

get_changed_components() {
    CHANGE_FILE=$1

    for directory in $(cat $CHANGE_FILE | grep "components" | cut -d/ -f 1-3 | uniq);
    do
        echo $directory
    done
}

TEST_FILE=".ci/test.sh"

component_has_tests() {
    COMPONENT=$1

    [ -f $COMPONENT/$TEST_FILE ]; 
}