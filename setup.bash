#!/bin/bash

set -e

# Load env variables (optional improvement)
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Build image
docker build -t purpleair-client .

# Run container
docker run --rm -it \
    --env PURPLEAIR_API_KEY=$PURPLEAIR_API_KEY \
    purpleair-client
