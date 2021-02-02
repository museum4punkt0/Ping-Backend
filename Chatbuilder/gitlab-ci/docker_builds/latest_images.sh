#!/bin/sh

echo 'Login into images registry'
docker login -u gitlab-ci-token -p $CI_JOB_TOKEN registry.teamvoy.com

echo 'Show docker information'
docker info

echo 'Build new image'
docker build -t registry.teamvoy.com/$CI_PROJECT_PATH/chatbuilder:staging .

if [ $? -eq 0 ]; then
  echo 'Success: build new staging image.'
  echo '============================================'
  echo 'Push new image into registry with tag latest'
  docker push registry.teamvoy.com/$CI_PROJECT_PATH/chatbuilder:staging
else
  echo 'Failure: build new staging image. Script failed'
  exit 1
fi
