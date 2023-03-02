FROM node:17-alpine3.14


WORKDIR /usr/src/webapp
RUN echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf

COPY ./svelte.config.js ./
COPY ./vite.config.js ./
COPY ./package*.json ./

RUN npm install
RUN npm update

USER root
COPY ./ ./

EXPOSE 3000

ENV HOST=0.0.0.0

CMD npm run dev