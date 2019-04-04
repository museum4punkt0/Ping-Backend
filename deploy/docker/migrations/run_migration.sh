#!/bin/bash

set -e

function run_migration() {

  local aws_region='eu-central-1'

  local option
  while getopts k:a:s:t:c: option; do
    case "$option" in
      k)
        local env_prefix="$OPTARG"
        ;;
      a)
        export AWS_SES_ACCESS_KEY_ID="$OPTARG"
        ;;
      s)
        export AWS_SES_SECRET_ACCESS_KEY="$OPTARG"
        ;;
      t)
        local tag="$OPTARG"
        ;;
      c)
        export CIRCLE_BRANCH="$OPTARG"
        ;;
      *)
        echo 'Ensure you have right environment variables'
        exit 1
        ;;
    esac
  done

  function get_parameter() {

    local aws_region='eu-central-1'
    local env_prefix="${1}"
    local param_name="${2}"
    aws ssm get-parameters --names "${env_prefix}.${param_name}" --with-decryption --region "$aws_region" | jq -r '.Parameters[]' | jq -r .Value
  }

  while read line
    do eval "export ${line}='$(get_parameter ${env_prefix} ${line})'"
  done < deploy/environments/${env_prefix}_environments_migrate.txt

  local login=$(aws ecr get-login --region "$aws_region" --no-include-email)
  ${login}

  cd deploy/docker/migrations

  docker-compose up -d

  docker cp ip_to_aws.sh python:/.
  docker exec -it python 'bash' '/ip_to_aws.sh'
  docker exec -it python './manage.py' 'migrate'

}

run_migration "$@"

