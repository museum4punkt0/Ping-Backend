#!/bin/sh

echo 'Login into images registry'
docker login -u gitlab-ci-token -p $CI_JOB_TOKEN registry.teamvoy.com

echo 'Fetch release version'
export version=`echo "$CI_COMMIT_REF_NAME" | sed "s/\//-/g"`

echo 'Build new image with version'
docker build -t registry.teamvoy.com/$CI_PROJECT_PATH/chatbuilder:$version .

if [ $? -eq 0 ]; then
  echo 'Success: build new demo image.'
  echo '============================================'
  echo 'Push new image into registry with version'
  docker push registry.teamvoy.com/$CI_PROJECT_PATH/chatbuilder:$version
else
  echo 'Failure: build new demo image. Script failed'
  exit 1
fi
