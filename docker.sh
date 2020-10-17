#!/bin/bash
################################################################################
# docker.sh - A helper script to run common docker commands for this project.
#
# Usage: $ ./docker.sh <help|build|run|clean>

# Copyright (C) 2020  S.G. Skinner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################


#
# Print help info when asked to or when `command` is invalid
#
function _usage() {
    echo "$ ./docker.sh <help|build|run|clean>"
    echo "     help: Print these lines"
    echo "    build: Rebuild docker image for when Dockerfile changes"
    echo "      run: Start a new container from a built image"
    echo "    clean: Delete all dangling images, i.e., non-tagged"
}


#
# Create and start a new container from the latest sgs/python-utils image.
#
function _run() {
    docker run \
        -d \
        -v "$HOME/git/line_monitor/app:/usr/src/app" \
        -e TARGET_HOST="$TARGET_HOST" \
        --rm \
        --name line_monitor \
        sgskinner/line_monitor:latest
}


#
# Build/rebuild a new image from the Dockerfile. Note this will 'steal' the tag
# from the current image if it exists. This means the old image will have a name
# that is the same as its id in the `$ docker images` list. Use `_clean` to clear
# out these orphaned images.
#
function _build() {
    docker build \
    --file Dockerfile \
    --tag sgskinner/line_monitor:latest \
    .
}


#
# Prune (delete) all images that are 'dangling', i.e., has no associated
# container and has not tagged name. These are the images in the
# '$ docker images` list where name and id are the same. These become
# dangling by way of a new build always tagging the image as
# 'sgs/python-sandbox:latest` -- only the latest build will retain the tag.
#
function _clean() {
    # shellcheck disable=SC2046
    docker rmi $(docker images -f "dangling=true" -q)
}


#
# Driver function, reads user command and executes the related function.
#
function main() {
    if [[ $# -lt 1 ]]; then
        _usage
        exit 1
    fi
    command="$1"

    case "$command" in
    'run')
        _run
        ;;
    'build')
        _build
        ;;
    'clean')
        _clean
        ;;
    'help')
        _help
        ;;
    *)
        _usage
        ;;
    esac
}

main "$@"
