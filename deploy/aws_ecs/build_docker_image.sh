#!/bin/bash

set -e

function build_push_image() {

  while getopts k:a:s:t: option; do
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
  done < deploy/environments/${env_prefix}_environments_ecs.txt

  login=$(aws ecr get-login --region eu-central-1 --no-include-email)
  ${login}

  cp deploy/docker/python/Dockerfile .
  envsubst '$SERVICE_NAME' < deploy/docker/nginx/default.temp > deploy/docker/nginx/default.conf
  docker build -t 081960884429.dkr.ecr.eu-central-1.amazonaws.com/"${ENVIRONMENT}"_images:nginx_"${CIRCLE_WORKFLOW_ID}" deploy/docker/nginx/.
  docker build -t 081960884429.dkr.ecr.eu-central-1.amazonaws.com/"${ENVIRONMENT}"_images:python_"${CIRCLE_WORKFLOW_ID}" .
  docker push 081960884429.dkr.ecr.eu-central-1.amazonaws.com/"${ENVIRONMENT}"_images:python_"${CIRCLE_WORKFLOW_ID}"
  docker push 081960884429.dkr.ecr.eu-central-1.amazonaws.com/"${ENVIRONMENT}"_images:nginx_"${CIRCLE_WORKFLOW_ID}"

}

build_push_image "${@}"
