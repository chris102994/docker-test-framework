#!/bin/bash

set -u # Unset Variables are an error
set -e # Exit on error

###
# This script uses the common_tools/script/ single-function 
# Scripts to build, test, and deploy docker containers to the
# Official docker registry.
###

usage() {
	echo "
usage: $(basename "$0") [OPTIONS]  
-b, --build   - Build: (Default=false) Build the container with the given options.
-e, --envfile - Environment File: path/to/env_file.env to load.
-h. --help    - Help: prints usage.
-p, --pushdr  - Push To Registry: (Default=false) Pushes the container to the official docker registry.
-r, --pushrm  - Push README: (Default=false) Pushes the README.md to your docker registry page.
-g, --pushgt  - Push Git Version Tag: (Default=false) Pushes the updated git tag from the versioning script to github.
	"
	exit 1
}

# Transform long options to short ones
for arg in "$@"; do
  shift
  case "$arg" in
    '-build'|'--build')       set -- "$@" "-b" ;;
    '-envfile'|'--envfile')   set -- "$@" "-e" ;;
    '-help'|'--help')         set -- "$@" "-h" ;;
    '-pushdr'|'--pushdr')     set -- "$@" "-p" ;;
    '-pushrm'|'--pushrm')     set -- "$@" "-r" ;;
    '-pushgt'|'--pushgt')     set -- "$@" "-g" ;;
    * )        		      set -- "$@" "$arg"
  esac
done

# Default options
BUILD='false'
ENV=''
PUSH_README_TO_REGISTRY='false'
PUSH_TO_REGISTRY='false'
PUSH_GIT_TAG='false'

# Sort through options
while getopts 'be:hprg' 'option'; do
	case "${option}" in
		'b') BUILD='true' ;;
		'e') ENV="$ENV ${OPTARG}" ;;
		'h') usage ;;
		'p') PUSH_TO_REGISTRY='true' ;;
		'r') PUSH_README_TO_REGISTRY='true' ;;
		'g') PUSH_GIT_TAG='true' ;;
		 * ) usage ;;
	esac
done

echo "
##### ARGUMENTS #####
Build				(-b, --build): ${BUILD}
Environment File(s)		(-e, --envfile): ${ENV}
Push To Docker Registry		(-p, --pushdr): ${PUSH_TO_REGISTRY}
Push README to Docker Registry	(-r, --pushrm): ${PUSH_README_TO_REGISTRY}
Push Git Version Tag		(-g, --pushgt): ${PUSH_GIT_TAG}
#####################
"

# Submodule could be named anything - Let's be smart.
SCRIPTS_DIR=$(grep -B1 "url = https://github.com/chris102994/common_tools" .gitmodules | grep path | sed 's#.*= ##')/scripts

# Load the env files
source $SCRIPTS_DIR/load_env_files.sh $ENV

# Version
source $SCRIPTS_DIR/versioning.sh || true

# Build
if [ "$BUILD" = true ]; then
	$SCRIPTS_DIR/make_container.sh
fi

# Push the image to the registry
if [ "$PUSH_TO_REGISTRY" = true ]; then
	$SCRIPTS_DIR/push_to_registry.sh
fi

# Push the readme to the registry
if [ "$PUSH_README_TO_REGISTRY" = true ]; then
	$SCRIPTS_DIR/push_readme_to_dockerhub.sh
fi

# Push the git tag to github
if [ "$PUSH_GIT_TAG" = true ]; then
	$SCRIPTS_DIR/push_git_tag.sh
fi
