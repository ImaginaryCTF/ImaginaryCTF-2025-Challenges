# syntax=docker/dockerfile:1

FROM node:24-alpine

ENV NODE_ENV=production
ENV FLAG=ictf{fake_flag_for_testing}

WORKDIR /app

COPY --chown=node package*.json ./

RUN npm install --production

USER node

COPY . .

EXPOSE 3000

CMD ["node", "index.js"]
