FROM node:lts-alpine AS setup
WORKDIR /app

COPY ["package.json", "yarn.lock", "./"]
RUN yarn && \
    yarn cache clean

COPY . .

FROM node:lts-alpine AS build-stage
WORKDIR /build

COPY --from=setup /app .
RUN yarn build

FROM caddy:2-alpine as caddy
WORKDIR /etc/caddy

COPY --from=build-stage /build/dist /app
COPY ./caddy/Caddyfile.prod ./Caddyfile
