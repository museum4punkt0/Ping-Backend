#!/bin/bash

set -e

function deploy_task(){

  local scale_count
  local autoscale_group_name
  local revision_arn
  local cluster_arn
  local aws_region='eu-central-1'
  local cluster_name="${1}"

  scale_count=$(aws ecs list-container-instances --cluster "$cluster_name" --region "$aws_region" | jq '.containerInstanceArns[]' | wc -l)
  autoscale_group_name=$(aws autoscaling describe-tags --region "$aws_region" | jq -r '.Tags[] | select(.ResourceId | contains ("'$cluster_name'")) | .ResourceId' | sed -n '1p')
  aws autoscaling set-desired-capacity --auto-scaling-group-name "$autoscale_group_name" --desired-capacity $((scale_count+scale_count)) --region "$aws_region" --no-honor-cooldown || \
  aws autoscaling set-desired-capacity --auto-scaling-group-name "$autoscale_group_name" --desired-capacity $((scale_count+1)) --region "$aws_region" --no-honor-cooldown || true
  timeout 5m bash deploy/aws_ecs/blue-green.sh -c check-launch -k "${cluster_name}" -t "${CIRCLE_WORKFLOW_ID}" -a "${AWS_ACCESS_KEY_ID}" -s "${AWS_SECRET_ACCESS_KEY}"
  aws ecs register-task-definition --cli-input-json file://ecs_taks_definition.json  --region "$aws_region"
  revision_arn=$(aws ecs list-task-definitions --family-prefix "$cluster_name"  --region "$aws_region" | jq --raw-output --exit-status '.taskDefinitionArns[-1]')
  cluster_arn=$(aws ecs list-clusters --region "$aws_region" | jq --raw-output --exit-status '.clusterArns[]' | grep "$cluster_name")
  aws ecs update-service --cluster "$cluster_arn" --service "$cluster_name" --task-definition "$revision_arn" --region "$aws_region"

}

function generate_task_definition() {

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
  done < deploy/environments/${env_prefix}_environments_ecs.txt

  export TAG="${CIRCLE_WORKFLOW_ID}"

  envsubst < deploy/aws_ecs/ecs_task_definition.json.tmp > ecs_taks_definition.json

  deploy_task "${CLUSTER_NAME}"

}

generate_task_definition "${@}"
