FROM node:20-alpine

WORKDIR /app

COPY app/package*.json ./

RUN npm install

COPY app ./app

RUN npm run build

EXPOSE 3000

CMD ["sh", "-c", "npm run start"]
