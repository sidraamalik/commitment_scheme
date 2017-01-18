#!/bin/bash

curl -v localhost:8000/messages/1/reveal \
    -H 'Content-type: application/json' \
    -X POST \
    -d '{"secret": "secret"}' \
    -H "Authorization: $(echo 'subir@jolly.com:password' | base64)"
