FROM node:lts-alpine AS setup
WORKDIR /app

COPY ["package.json", "yarn.lock", "./"]
RUN yarn && \
    yarn cache clean

COPY . .

FROM setup AS build
RUN yarn build

FROM caddy:2-alpine as caddy
WORKDIR /etc/caddy

COPY --from=build-stage /app/dist /app
COPY ./caddy/Caddyfile.prod /etc/caddy/Caddyfile
