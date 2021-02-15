#!/bin/bash

set -e

function run_tests() {

  local option
  while getopts k:a:s: option; do
    case "$option" in
      k)
        local env_prefix="$OPTARG"
        ;;
      a)
        export AWS_ACCESS_KEY_ID="$OPTARG"
        ;;
      s)
        export AWS_SECRET_ACCESS_KEY="$OPTARG"
        ;;
      *)
        echo 'Ensure you have right environment variables'
        exit 1
        ;;
    esac
  done

  function get_parameter() {

    local aws_region='eu-central-1'
    local kms_key="${1}"
    local param_name="${2}"
    aws ssm get-parameters --names "${kms_key}.${param_name}" --with-decryption --region "$aws_region" | jq -r '.Parameters[]' | jq -r .Value
  }

  while read line
    do eval "export ${line}='$(get_parameter ${env_prefix} ${line})'"
  done < deploy/environments/${env_prefix}_environments_test.txt

  local aws_region='eu-central-1'
  local ecr_repo="350016030663.dkr.ecr.us-west-2.amazonaws.com/${ENVIRONMENT}_images"

  login=$(aws ecr get-login --region eu-central-1 --no-include-email)
  ${login}


  cd deploy/docker/test
  docker-compose up -d
  sleep 10
  docker exec -it python './manage.py' 'test'

  declare -a local images=(
    python
    nginx
  )

  if !([ "$CIRCLE_BRANCH" == "master" ] || [ "$CIRCLE_BRANCH" == "qa" ] || [ "$CIRCLE_BRANCH" == "stage" ])
  then
    echo 'Deleting images for test branches'
    for images in ${images[@]}; do
      aws ecr batch-delete-image --repository-name "${ENVIRONMENT}_images" --image-ids imageTag=${images}_${CIRCLE_WORKFLOW_ID} --region "$aws_region"
    done
  fi

}

run_tests "${@}"
