#!/usr/bin/env bash

set -e

SCRIPT_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# Pre-pre-flight? 🤷
if [[ -n "$MSYSTEM" ]]; then
    echo "Seems like you are using an MSYS2-based system (such as Git Bash) which is not supported. Please use WSL instead."
    exit 1
fi

source $SCRIPT_PATH/../docker/.env

DOCKER_VERSION=$(docker version --format '{{.Server.Version}}')
VERSION_PARTS=(${DOCKER_VERSION//./ })

if ((${VERSION_PARTS[0]} < 24 || (${VERSION_PARTS[0]} == 0 && ${VERSION_PARTS[1]} < 0))); then
    COMPOSE_COMMAND='docker-compose'
else
    COMPOSE_COMMAND='docker compose'
fi

if [ "$ENV" == "production" ]; then
    $COMPOSE_COMMAND --project-name=${PROJECT} -f $SCRIPT_PATH/../docker/docker-compose.yml -f $SCRIPT_PATH/../docker/docker-compose.prod.yml -f $SCRIPT_PATH/../docker/docker-compose.backup.yml "$@"
else
    $COMPOSE_COMMAND --project-name=${PROJECT} --project-directory=$SCRIPT_PATH/../docker -f $SCRIPT_PATH/../docker/docker-compose.yml -f $SCRIPT_PATH/../docker/docker-compose.override.yml "$@"
fi
