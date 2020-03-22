#!/bin/bash

# Tools script to get various bits of information.

# These 3 flags can be set as an ENV variable OR the git commit message to bump the correlating version
# BUMP_MAJOR
# BUMP_MINOR
# BUMP_PATCH

GIT_VERSION=$(git describe --tags)
if [ $? -eq 0 ]; then
    GIT_VERSION=$(echo $GIT_VERSION |  egrep -o '[0-9]*\.[0-9]*\.[0-9]*' )
    MAJOR_VERSION=$(echo $GIT_VERSION | cut -d. -f1)
    MINOR_VERSION=$(echo $GIT_VERSION | cut -d. -f2)
    PATCH_VERSION=$(echo $GIT_VERSION | cut -d. -f3)
fi

# Default Versioning
MAJOR_VERSION=${MAJOR_VERSION:-1}
MINOR_VERSION=${MINOR_VERSION:-0}
PATCH_VERSION=${PATCH_VERSION:-0}

# Check if ANY bump's are set in the ENV or MSG AND IF they ARE then Bump that version
GIT_MESSAGE=$(git show -s --format=%s | tr a-z A-Z)
if [ "${BUMP_MAJOR:-UNSET}" != "UNSET" ] && [ "${BUMP_MAJOR,,}" = true ] || [[ "$GIT_MESSAGE" =~ .*"BUMP_MAJOR".* ]]; then
    BUMP_MAJOR=true
    ((MAJOR_VERSION+=1))
    MINOR_VERSION=0
    PATCH_VERSION=0
    echo "Major Version Bumped to: $MAJOR_VERSION"
elif [ "${BUMP_MINOR:-UNSET}" != "UNSET" ] && [ "${BUMP_MINOR,,}" = true ] || [[ "$GIT_MESSAGE" =~ .*"BUMP_MINOR".* ]]; then
    BUMP_MINOR=true
    ((MINOR_VERSION+=1))
    PATCH_VERSION=0
    echo "Minor Version Bumped to: $MINOR_VERSION"
elif [ "${BUMP_PATCH:-UNSET}" != "UNSET" ] && [ "${BUMP_PATCH,,}" = true ] || [[ "$GIT_MESSAGE" =~ .*"BUMP_PATCH".* ]]; then
    BUMP_PATCH=true
    ((PATCH_VERSION+=1))
    echo "Patch Bumped to: $PATCH_VERSION"
else
    echo "Non-Versioned build. Keeping previous version."
    BUMP_MAJOR=false
    BUMP_MINOR=false
    BUMP_PATCH=false
fi

# Just some handy tools we can export.
DATE=$(date)
EPOCH=$(date "+%s")
# This ensures that if we're building on travis ci we will get the proper branch -- Detached git state.
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD | sed "s#HEAD#$TRAVIS_BRANCH#i")
GIT_COMMIT=$(git rev-parse --short HEAD)
GIT_REPO=$(git config --get remote.origin.url | grep -Po "(?<=git@github\.com:)(.*?)(?=.git)" | sed 's#.*/##')
# Sometimes this doesn't work. This will assume the name is that of the containing folder.
GIT_REPO="${GIT_REPO:-$(basename $(git rev-parse --show-toplevel))}"
GIT_VERSION="v${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}"

# We need to know in the build process if we bumped. This variable lets us ensure it gets pushed properly.
if [ "$BUMP_MAJOR" = true ] || [ "$BUMP_MINOR" = true ] || [ "$BUMP_PATCH" = true ]; then
    PUSH_TAG=true
else
    GIT_VERSION="$GIT_VERSION-testing"
fi

# Export everything
export DATE=$DATE
export EPOCH=$EPOCH
export GIT_BRANCH=$GIT_BRANCH
export GIT_COMMIT=$GIT_COMMIT
export GIT_REPO=$GIT_REPO
export GIT_VERSION=$GIT_VERSION
export IMAGE_TAG=${IMAGE_TAG:-UNSET}-$GIT_VERSION
export MAJOR_VERSION=$MAJOR_VERSION
export MINOR_VERSION=$MINOR_VERSION
export PATCH_VERSION=$PATCH_VERSION
export PUSH_TAG=${PUSH_TAG:-false}
