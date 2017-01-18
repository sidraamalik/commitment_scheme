#!/bin/bash

curl -v localhost:8000/messages \
    -H 'Content-type: application/json' \
    -X POST \
    -d '{"message": "mymessage!", "secret": "secret"}' \
    -H "Authorization: $(echo 'subir@jolly.com:password' | base64)"
