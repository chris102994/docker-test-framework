# This is a helper submodule meant for snippets of code used in multiple projects.

Builds and deploys containers and supports versioning.

## Example CI Scripts to use this submodule:
* [.travis.yml](https://github.com/chris102994/common_tools/blob/master/examples/.travis.yml)

## Scripts:

### [.ci_vars.yml](https://github.com/chris102994/common_tools/blob/master/scripts/.ci_vars.yml)
This is a YAML file that contains some basic environment variables needed in your CI cycle to properly utilize the following scripts.

### [load_env_files.sh](https://github.com/chris102994/common_tools/blob/master/scripts/load_env_files.sh)
This is a script that can take any number of env files and load them into the environment for you.

### [make_container.sh](https://github.com/chris102994/common_tools/blob/master/scripts/make_container.sh)
This is a script that can make a container for you from the given environment variables of:
* BASE_IMAGE
* DATE
* DOCKER_FILE
* DOCKER_NAME
* DOCKER_REPO
* GIT_VERSION
* GIT_COMMIT
* IMAGE_TAG
* LATEST_TAG

### [push_git_tag.sh](https://github.com/chris102994/common_tools/blob/master/scripts/push_git_tag.sh)
This is a script that works with `versioning.sh`. This will push a git tag for the new version based on the environment variables.

### [push_readme_to_dockerhub.sh](https://github.com/chris102994/common_tools/blob/master/scripts/push_readme_to_dockerhub.sh)
This is a script that will push the README.md from the git project to the docker hub project page.

### [push_to_registry.sh](https://github.com/chris102994/common_tools/blob/master/scripts/push_to_registry.sh)
This is a script that works with `make_container.sh`. This will push the containers that script makes.

### [versioning.sh](https://github.com/chris102994/common_tools/blob/master/scripts/versioning.sh)
This is a script that can version build artifacts for you based on the git tags!
</br>
**To bump a version in any future build you just have to say it in your commit message:**
* BUMP_MAJOR
* BUMP_MINOR
* BUMP_PATCH

**This will export the following environment variables:**

* DATE
* EPOCH
* GIT_BRANCH
* GIT_COMMIT
* GIT_REPO
* GIT_VERSION
  * MAJOR_VERSION
  * MINOR_VERSION
  * PATCH_VERSION
* IMAGE_TAG=$IMAGE_TAG-$GIT_VERSION
* PUSH_TAG - If there was a version bump - Used to determine to push a new tag to git.

Versioning is in the format of: `v${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}` - If none of these are bumped then the versioning script assumes that you're building for testing purposes and appends a `-testing` to the end of the version.
