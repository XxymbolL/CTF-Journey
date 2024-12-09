#!/bin/bash

# Ensure the script is executed from its own directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
CTF_DOCKER_DIR="$SCRIPT_DIR/CTF-Docker"

# Check if the CTF-Docker directory exists
if [[ ! -d "$CTF_DOCKER_DIR" ]]; then
  echo "CTF-Docker directory not found in $SCRIPT_DIR. Please ensure the correct structure."
  exit 1
fi

# Docker configurations
IMAGE_NAME="ctf-base"
CONTAINER_NAME="ctf-container"

# Build the Docker image if it doesn't exist
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
  echo "Docker image $IMAGE_NAME not found. Building it..."
  docker build --platform linux/amd64 -t $IMAGE_NAME "$CTF_DOCKER_DIR"
fi

# Check if the container is already running
if [[ "$(docker ps -q -f name=$CONTAINER_NAME)" ]]; then
  echo "Container $CONTAINER_NAME is already running. Attaching..."
  docker exec -it $CONTAINER_NAME /bin/bash
else
  # Run the container with explicit platform set to x86_64 (amd64)
  echo "Starting new container $CONTAINER_NAME..."
  docker run -it --platform linux/amd64 --name $CONTAINER_NAME \
    -v "$SCRIPT_DIR:/ctf/CTF-Journey" \
    $IMAGE_NAME
fi

# Clean up the stopped container on exit
docker rm $CONTAINER_NAME

