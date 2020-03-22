#!/bin/bash

set -u # Unset Variables are an error
set -e # Exit on error

if [ "${PUSH_TAG:-UNSET}" != "UNSET" ] && [ "${PUSH_TAG,,}" = true ]; then
	curl \
		-v \
		-s \
		-H "Authorization: token $GIT_TOKEN" \
		-H "Content-Type:application/json" \
		--data '{ "user" : { "email" : "$GIT_EMAIL", "password" : "$GIT_TOKEN" },
				  "tag_name": "'$GIT_VERSION'",
				  "target_commitish": "'$GIT_BRANCH'",
				  "name": "'$GIT_VERSION'",
				  "body": "CI Release of '$GIT_VERSION'",
				  "draft": false, 
				  "prerelease": false}' \
		"https://api.github.com/repos/$GIT_USERNAME/$GIT_REPO/releases"
fi