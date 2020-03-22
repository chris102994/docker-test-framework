#!/bin/bash

set -u # Unset Variables are an error
set -e # Exit on error

DOCKER_REPO_URL="https://hub.docker.com/v2/repositories/$DOCKER_USERNAME/$DOCKER_NAME/"
DOCKER_LOGIN_URL="https://hub.docker.com/v2/users/login"

TOKEN=$(curl \
		-s \
		-H "Content-Type: application/json" \
		-X POST \
		--data '{ "username" : "'$DOCKER_USERNAME'", "password" : "'$DOCKER_PASSWORD'" }' \
		$DOCKER_LOGIN_URL \
		| jq -r .token)

RESPONSE_CODE=$(curl \
				-v \
				-s \
				--write-out %{response_code} \
				--output /dev/null \
				-H "Authorization: JWT $TOKEN" \
				-X PATCH \
				--data-urlencode full_description@README.md \
				$DOCKER_REPO_URL)

if [ $RESPONSE_CODE -eq 200 ]; then
	echo "Successfully pushed README.md to $DOCKER_REPO_URL"
	exit 0
else
	echo "Unable to push README.md for $DOCKER_REPO_URL"
	exit 1
fi