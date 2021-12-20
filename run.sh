#!/bin/bash

docker-compose -f ./Cinema/docker-compose.yml  up --build -d
docker-compose -f ./booking/docker-compose.yml  up --build -d


