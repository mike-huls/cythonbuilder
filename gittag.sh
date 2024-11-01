#!/bin/bash

# Validate arguments
if [ "$#" -lt 1 ]; then
  echo "Error: You must provide exactly one argument."
  echo "Usage: $0 {acceptation|production|test}"
  exit 1
fi

# Iterate over all provided arguments
for arg in "$@"; do
  # Convert argument to lowercase
  arg=${arg,,}
  environment="null";

  # Validate argument and set environment
  if [ "$arg" == "production" ] || [ "$arg" == "prod" ] || [ "$arg" == "release" ]; then
    environment='production'
  elif [ "$arg" == "acceptation" ] || [ "$arg" == "acc" ]; then
    echo "Error: Invalid argument '$arg'. Accepted values are 'production', or 'test'."
    exit 1
  elif [ "$arg" == "test" ]; then
    environment='test';
  else
    echo "Error: Invalid argument '$arg'. Accepted values are 'acceptation', 'production', or 'test'."
    exit 1
  fi

  # Tag the environment
  tag=${environment}-build-$(date +'%Y%m%d%H%M%S')
  git tag ${tag};
  echo git push ${tag};

done
echo or
echo git push --tags;