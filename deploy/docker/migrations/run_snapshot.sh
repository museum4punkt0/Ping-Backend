#!/bin/bash

set -e

readonly storing_time='1296000' # 15 days to store snapshot
readonly arn_prefix='arn:aws:rds:us-west-2:081960884429:snapshot:'

declare -a db_names=(
  meinobjekt
)

function delete_old_snapshots() {
  local aws_region="${1}"
  local current_time=$(date +%s)
  local snapshots_list=$(aws rds describe-db-snapshots --snapshot-type 'manual' --region "${aws_region}" | jq '.DBSnapshots[]' | jq -r '.DBSnapshotIdentifier' | awk /[0-9]+{10}$/)
  local snapshot_time
  local snapshot_age
  local snapshot
  local snapshot_tag
  for snapshot in ${snapshots_list}; do
    snapshot_time=$(awk -F '-' '{print $5}' <<< "${snapshot}")
    snapshot_age=$(( ${current_time} - ${snapshot_time} ))
    snapshot_tag=$(aws rds list-tags-for-resource --resource-name "${arn_prefix}${snapshot}" --region "${aws_region}" | jq '.TagList[]' | jq -r '.Value')
    if (( "${snapshot_age}" >= "${storing_time}" )) && [ "${snapshot_tag}" == 'Deployment' ]; then
      aws rds delete-db-snapshot --db-snapshot-identifier "${snapshot}" --region "${aws_region}"
      echo "Deleting snapshot ${snapshot}"
    fi
  done
}

function create_new_snapshots() {
  local db_instances_names="${1}"
  local aws_region="${2}"
  local db_instance
  local snapshot_name
  local snapshot_names
  for db_instance in ${db_instances_names}; do
    snapshot_name="${db_instance}-deploy-$(date +%s)"
    snapshot_names+=" ${snapshot_name}"
    aws rds create-db-snapshot --db-instance-identifier "${db_instance}" --db-snapshot-identifier "${snapshot_name}" --tags "Key=Source,Value=Deployment" --region "${aws_region}"
  done

  for snapshot_name in ${snapshot_names}; do
    echo "Waiting for ${snapshot_name} snapshot creation"
    aws rds wait db-snapshot-completed --db-snapshot-identifier "${snapshot_name}" --region "${aws_region}"
  done

}

function get_db_instance_names() {
  local env_name="${1}"
  local instance
  for instance in ${db_names[@]}; do
    echo "${env_name}-${instance}"
  done
}

function main() {

  local option
  while getopts k:r: option; do
    case "${option}" in
      k)
        local env_prefix="${OPTARG}"
        ;;
      r)
        local aws_region="${OPTARG}"
        ;;
      *)
        echo 'Wrong arguments passed'
        exit 1
        ;;
    esac
  done

  delete_old_snapshots "${aws_region}"

  local db_instances_names
  if [ "${env_prefix}" == 'prod.meinobjekt' ]; then
    db_instances_names=$(get_db_instance_names 'prod')
  elif [ "${env_prefix}" == 'qa.meinobjekt' ]; then
    db_instances_names=$(get_db_instance_names 'qa')
  fi

  create_new_snapshots "${db_instances_names}" "${aws_region}"

}

main "$@"
