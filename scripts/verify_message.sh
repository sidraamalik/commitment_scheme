#!/bin/bash

curl -v localhost:8000/messages/2/verify \
    -H 'Content-type: application/json' \
    -X POST \
    -d '{"username": "subir@jolly.com"}' \
    -H "Authorization: $(echo 'subir@jolly.com1:password' | base64)"
