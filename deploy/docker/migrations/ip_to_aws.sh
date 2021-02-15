#!/bin/bash

set -e

#Configurations for security group id and aws region
readonly security_group_id='sg-0db999e958a7540bc'
readonly aws_region='eu-central-1'

function install_deps() {

  apt-get update && apt-get install -y python3 curl jq gettext git bash
  curl -O https://bootstrap.pypa.io/get-pip.py
  python3 get-pip.py --user
  /root/.local/bin/pip install awscli --upgrade --user

}

#Flush all old ips from circleci security group
function rm_ip_from_aws() {

  local binary='/root/.local/bin/aws'
  local current_security_group=$("$binary" ec2 describe-security-groups --region "${aws_region}" --group-id "${security_group_id}")
  local ip_count=$(echo "${current_security_group}" | jq -r '.SecurityGroups[0].IpPermissions | length')
  if [ "${ip_count}" > 0 ]; then
    for (( n=0; n < "$ip_count"; n++ ))
    do
      local this_port=$(echo "${current_security_group}" | jq -r '.SecurityGroups[0].IpPermissions['"$n"'].FromPort')
      local cidr_count=$(echo "${current_security_group}" | jq -r '.SecurityGroups[0].IpPermissions['"$n"'].IpRanges | length')
      for (( c=0; c<"${cidr_count}"; c++ ))
      do
        local this_cidr=$(echo "${current_security_group}" | jq -r '.SecurityGroups[0].IpPermissions['"$n"'].IpRanges['"$c"'].CidrIp')
        "$binary" ec2 revoke-security-group-ingress --region "${aws_region}" --group-id "${security_group_id}" --protocol tcp --port "${this_port}" --cidr "${this_cidr}"
      done
    done
  fi

}

#Add current server IP to aws security group
function add_ip_to_aws() {

  local binary='/root/.local/bin/aws'
  local public_ip_address=$(wget -qO- http://checkip.amazonaws.com)
  "$binary" ec2 authorize-security-group-ingress --region "${aws_region}" --group-id "${security_group_id}" --protocol tcp --port 5432 --cidr "$public_ip_address"/32

}

install_deps
rm_ip_from_aws
add_ip_to_aws
