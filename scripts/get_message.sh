#!/bin/bash

curl -v localhost:8000/messages/1 \
    -H 'Content-type: application/json' \
    -H "Authorization: $(echo 'subir@jolly.com:password' | base64)"
