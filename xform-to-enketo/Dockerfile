FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN apk update && apk add python3 make g++

RUN npm install

COPY . .

EXPOSE 5261

CMD ["node", "server.js"]
