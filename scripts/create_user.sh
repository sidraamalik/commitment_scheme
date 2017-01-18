#!/bin/bash
curl -v localhost:8000/users \
    -X POST \
    -H 'Content-type: application/json' \
    -d '{"user": "subir@jolly.com", "password": "password"}'
