#!/bin/bash

set -u # Unset Variables are an error
set -e # Exit on error

GIT_REPO_URL="docker.pkg.github.com"

echo "Pushing to official docker registry"
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker push "$DOCKER_REPO"/"$DOCKER_NAME":"$IMAGE_TAG"
docker push "$DOCKER_REPO"/"$DOCKER_NAME":"$LATEST_TAG"

echo "Pushing to github docker registry"
echo "$GIT_TOKEN" | docker login "$GIT_REPO_URL" -u "$GIT_USERNAME" --password-stdin

docker push "$GIT_REPO_URL"/"$GIT_USERNAME"/"$DOCKER_NAME"/"$DOCKER_NAME":"$IMAGE_TAG"
docker push "$GIT_REPO_URL"/"$GIT_USERNAME"/"$DOCKER_NAME"/"$DOCKER_NAME":"$LATEST_TAG"
