set -e

# Pull docker images from remote registry
IMAGE="registry.teamvoy.com/mein-object/chatbuilder/chatbuilder:$release_tag"
docker pull $IMAGE

# Create reverse-proxy network
# docker network create CHANGE_ME -d overlay || echo 0

docker stack deploy --prune --resolve-image always --with-registry-auth -c $composes_folder/docker-compose.$node_env.yaml $node_env"_"$project

