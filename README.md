 
## [chris102994/docker-test-framework](https://github.com/chris102994/docker-test-framework)

[![Build Status](https://travis-ci.com/chris102994/docker-test-framework.svg?branch=master)](https://travis-ci.com/chris102994/docker-test-framework)
[![Microbadger Size & Layers](https://images.microbadger.com/badges/image/christopher102994/docker-test-framework.svg)](https://microbadger.com/images/christopher102994/docker-test-framework "Get your own image badge on microbadger.com")
[![Image Pulls](https://img.shields.io/docker/pulls/christopher102994/docker-test-framework)](https://hub.docker.com/repository/docker/christopher102994/docker-test-framework)
 [![Alpine](https://images.microbadger.com/badges/version/christopher102994/docker-test-framework:latest.svg)](https://microbadger.com/images/christopher102994/docker-test-framework:latest "Microbadger info for Alpine Test Container")
[![GitHub tag Version](https://img.shields.io/github/v/tag/chris102994/docker-test-framework?label=Version&style=plastic)](https://chris102994.github.io/containers/)


## Outside Packages
* Built on my [base image](https://github.com/chris102994/docker-base-image)
    * [Selenium](https://github.com/SeleniumHQ/selenium) - API that allows browser emulation with chrome webdrivers.
    * [Jinja2](https://palletsprojects.com/p/jinja/) - Documentation template engine.
    * [ShellCheck](https://github.com/koalaman/shellcheck) - Static analysis tool for shell scripts.

## Docker
```
docker run \
	--name=docker-test-framework \
	-e DOCKER_NAME="docker-test-framework" \
	-e DOCKER_REPO="myname" \
	-e ENV_VARS="THIS=THAT,X=Y" \
	-e GIT_EMAIL="myemail@server.com" \
	-e GIT_TOKEN="mysupersecrettoken" \
	-e GIT_VERSION="v1.0.0" \
	-e GUI="true" \
	-e SSL="false" \
	-e PORT="5700" \
	-e TAGS="latest, ubuntu-18-latest" \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v $(pwd):/workspace \
	christopher102994/docker-test-framework:latest
```

## Parameters
Container specific parameters passed at runtime. The format is `<external>:<internal>` (e.g. `-p 443:22` maps the container's port 22 to the host's port 443).

| Parameter | Function |
| -------- | -------- |
| -e DOCKER_NAME | Name of the docker container. |
| -e DOCKER_REPO | Name of the user the docker container is hosted under. |
| -e DOCKER_SLEEP | Time to sleep after setting up container testing. (Default=60s) |
| -e ENV_VARS | Comma separated list of env vars to map to the container being tested. i.e. (THIS=THAT,X=Y) |
| -e GIT_EMAIL | The email of the git user. |
| -e GIT_TOKEN | The token for the git user. |
| -e GIT_VERSION | The version of the container. Needed to keep file structure clean. Provided by tools/scripts/versioning.sh |
| -e GUI | (true|false) If a selenium GUI test should be performed or not. (Default=false) |
| -e SSL | (true|false) If a selenium GUI test is performed will it default to http or https protocol. (Default=false) |
| -e PORT | Port of web-gui for selenium GUI test. (Default=5700) |
| -e TAGS | A comma separated list of docker tags to test. |
| -e WEB_PATH | Path after proto://ip:port to open for a screenshot. (noVNC-Default=?autoconnect=true&resize=scale) |
| -v /var/run/docker.sock:/var/run/docker.sock | Needed for docker-in-docker testing. |
| -v /workspace| The location of your source code. Shellcheck will happen on all bash and shell files that reside here. |


## Application Setup

The admin interface is available at `http://<ip>:<port>/web/`

This will test the specified container and push the results to my [github page](https://github.com/chris102994/chris102994.github.io).
