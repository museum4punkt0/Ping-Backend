#! /bin/bash

set -e

function deployment_control() {

  local option
  while getopts c:k:t:a:s: option; do
    case "$option" in
      c)
        local action="$OPTARG"
        ;;
      k)
        local cluster_name="$OPTARG"
        ;;
      t)
        export TAG="$OPTARG"
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

  # Env variables that will be used for runtime scripts to check statuses
  local instance_launched='no'
  local task_launched='no'
  local deploy_completed='no'


  local aws_region='eu-central-1'
  local autoscale_group_name=$(aws autoscaling describe-tags --region "$aws_region" | jq -r '.Tags[] | select(.ResourceId | contains ("'$cluster_name'")) | .ResourceId' | sed -n '1p')
  local task_definition_number=$(aws ecs list-task-definitions --family-prefix "$cluster_name" --region "$aws_region" | jq --raw-output --exit-status '.taskDefinitionArns[-1]' | awk -F ":" '{print $7}')

  function check_instance_launched() {
    local aws_region='eu-central-1'
    local cluster_name="${1}"
    local autoscale_group_name="${2}"
    local current_count=$(aws ecs list-container-instances --cluster "$cluster_name" --region "$aws_region" | jq '.containerInstanceArns[]' | wc -l)
    local desired_count=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names "$autoscale_group_name" --region "$aws_region" | jq '.AutoScalingGroups[].DesiredCapacity')

    echo 'Checking is instance launched'
    if [ "$current_count" == "$desired_count" ]; then
      export instance_launched='yes'
    else
      sleep 30s
    fi
  }

  function check_task_launched() {
    local aws_region='eu-central-1'
    local cluster_name="${1}"
    local task_definition_number="${2}"
    local task_arns=$(aws ecs list-tasks --cluster "$cluster_name" --region "$aws_region" | jq -r '.taskArns[]')
    sleep 30s

    echo 'Checking is task launched'
    for task in ${task_arns[@]}; do
      curr_task_def_number=$(aws ecs describe-tasks --cluster "$cluster_name" --region "$aws_region" --tasks "$task" | jq -r '.tasks[].taskDefinitionArn' | awk -F ":" '{print $7}')
      if [ "$curr_task_def_number" == "$task_definition_number" ]; then
        export task_launched='yes'
      fi
    done
  }

  function check_deploy_completed() {
    local aws_region='eu-central-1'
    local cluster_name="${1}"
    local task_definition_number="${2}"
    local task_arns=$(aws ecs list-tasks --cluster "$cluster_name" --region "$aws_region" | jq -r '.taskArns[]')
    sleep 30s

    echo 'Checking is deploy completed'
    for task in ${task_arns[@]}; do
      curr_task_def_number=$(aws ecs describe-tasks --cluster "$cluster_name" --region "$aws_region" --tasks "$task" | jq -r '.tasks[].taskDefinitionArn' | awk -F ":" '{print $7}')
      if [ "$curr_task_def_number" != "$task_definition_number" ]; then
        return 0
      fi
    done
    export deploy_completed='yes'
  }

  if [ "$action" == 'blue-green' ]; then

    while [ "$instance_launched" == 'no' ]; do
      check_instance_launched "$cluster_name" "$autoscale_group_name"
    done
    echo 'Instance for deployment launched'

    while [ "$task_launched" == 'no' ]; do
      check_task_launched "$cluster_name" "$task_definition_number"
    done
    echo 'New deployment task launched'

    while [ "$deploy_completed" == 'no' ]; do
      check_deploy_completed "$cluster_name" "$task_definition_number"
    done
    echo 'Deployment completed'

  elif [ "$action" == 'check-launch' ]; then
    while [ "$instance_launched" == 'no' ]; do
    check_instance_launched "$cluster_name" "$autoscale_group_name"
    done
  fi

}

deployment_control "$@"
