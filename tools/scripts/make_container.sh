#!/bin/bash

set -u # Unset Variables are an error
set -e # Exit on error

GIT_REPO_URL="docker.pkg.github.com"

sudo docker build \
  --no-cache \
  --pull \
  --build-arg BASE_IMAGE="$BASE_IMAGE" \
  --build-arg BUILD_DATE="$DATE" \
  --build-arg VERSION="$GIT_VERSION" \
  --build-arg VCS_REF="$GIT_COMMIT" \
  -f "$DOCKER_FILE" \
  -t "$DOCKER_REPO"/"$DOCKER_NAME":"$IMAGE_TAG" \
  -t "$DOCKER_REPO"/"$DOCKER_NAME":"$LATEST_TAG" \
  -t "$GIT_REPO_URL"/"$GIT_USERNAME"/"$DOCKER_NAME"/"$DOCKER_NAME":"$IMAGE_TAG" \
  -t "$GIT_REPO_URL"/"$GIT_USERNAME"/"$DOCKER_NAME"/"$DOCKER_NAME":"$LATEST_TAG" \
  .
