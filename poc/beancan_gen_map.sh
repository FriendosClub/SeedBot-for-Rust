#!/bin/bash

URL_REGEX='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

TXTRED=$(tput setaf 1)
RESET=$(tput sgr0)

beancan_gen_map () {
    if [[ -z "$1" || -z "$2" ]]; then
        echo "Usage: beancan_gen_map <seed> <world size>"
    fi

    # We can input -1 for a random seed
    if [ $1 -lt 0 ]; then
        1="$(shuf -i 1-2147483647 -n 1)"
        echo "Using seed $1"
    fi

    # Get the CSRF token so the form works properly
    tokenField="$(curl -v -c cookies.txt -b cookies.txt http://beancan.io/map-generate 2>&1 | grep _token)"
    token="$(echo $tokenField | grep -Po '[^\s\\\"]{40}')"

    if [[ -z "$token" ]]; then
        echo "No CSRF token found!"
        return 1
    fi

    # Send the request to generate the map
    response="$(curl -v -c cookies.txt -b cookies.txt \
    -d "_token=$token&seed=$1&size=$2&level=Procedural+Map" \
    https://beancan.io/map-generate 2>&1)"

    url="$(echo $response | grep -m 1 -Po $URL_REGEX)"

    if [[ -z $url ]]; then
        echo -e "No URL found. Got response:\n$response"
    else
        echo "$TXTRED$url$RESET"
        echo "${TXTRED}https://beancan.io/maps/$1-$2${RESET}"
    fi
}
