include .env
.PHONY: test deploy test-on-image build-nginx

TMPFILE:=$(shell mktemp)
KEY_RSA?="key-rsa"
REMOTE_USER?="ubuntu"

start:
	docker-compose up

develop: start

start-prod:
	docker-compose -f docker-compose.yml \
		-f compose-files/docker-compose.images.override.yml \
		up

test:
	docker-compose -f docker-compose.yml \
		-f compose-files/docker-compose.override.yml \
		-f compose-files/docker-compose.test.override.yml up --exit-code-from backend

flush:
	docker-compose down -v --rmi all

restore-dump:
	cat dump.sql | PGPASSWORD=${DB_PASSWORD} docker-compose exec -T db psql -U ${DB_USERNAME}

test-on-images:
	docker-compose -f docker-compose.yml \
		-f compose-files/docker-compose.images.override.yml \
		-f compose-files/docker-compose.test.override.yml \
		up --exit-code-from backend

registry-login:
	docker login -u ${GITLAB_USER} -p ${GITLAB_TOKEN} registry.teamvoy.com

build-nginx:
	DOCKER_TOKEN=${GITLAB_TOKEN} \
	DOCKER_USER=${GITLAB_USER} \
	./scripts/build-nginx.sh

build-backend:
	DOCKER_TOKEN=${GITLAB_TOKEN} \
	DOCKER_USER=${GITLAB_USER} \
	./scripts/build-backend.sh


# provide an ability to change the user
deploy:
	ansible-galaxy install -r deploy/requirements.yml;
	ANSIBLE_HOST_KEY_CHECKING=False \
	ansible-playbook -v -i ${INSTANCE_IP}, --user ${REMOTE_USER} --private-key ${KEY_RSA} deploy/playbook.yml \
	--extra-vars "gitlab_user=${GITLAB_USER} gitlab_token=${GITLAB_TOKEN}"
	
# provide an ability to change the user
deploy-use-backup:
	ansible-galaxy install -r deploy/requirements.yml;
	ANSIBLE_HOST_KEY_CHECKING=False \
	ansible-playbook -v -i ${INSTANCE_IP}, --user ${REMOTE_USER} --private-key ${KEY_RSA} deploy/playbook-restore-backup.yml \
	--extra-vars "gitlab_user=${GITLAB_USER} gitlab_token=${GITLAB_TOKEN}"

service-file:
	docker-compose -f docker-compose.yml \
		-f docker-compose.images.override.yml \
		-f docker-compose.prod.override.yml \
	config > deploy/service.yml;

vagrant-provision:
	cd deploy; REGISTRY_TOKEN=${GITLAB_TOKEN} \
	REGISTRY_USER=${GITLAB_USER} \
	vagrant up --provision;

ssh-to-staging:
	ssh -i key_rsa ubuntu@${INSTANCE_IP}
