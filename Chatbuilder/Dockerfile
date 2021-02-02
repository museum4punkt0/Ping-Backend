FROM node:10-alpine

ARG NODE_ENV
ENV NODE_ENV=${NODE_ENV}

# set working directory
WORKDIR /app

# install app dependencies
COPY package*.json ./

COPY . .

RUN npm install 

RUN npm run build

RUN npm install -g serve

RUN npm install react-scripts@3.4.1 -g --silent


# start app
RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["docker-entrypoint.sh"]
