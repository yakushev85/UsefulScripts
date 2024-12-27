#!/usr/bin/env bash

# script for downloading from Youtube
# example: sudo ./yt-dl.sh https://www.youtube.com/watch?v=h8N9vh-x0IE

docker run --rm -i -e PGID=$(id -g) -e PUID=$(id -u) -v "$(pwd)":/workdir:rw mikenye/youtube-dl $1
