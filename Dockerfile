FROM node:18-alpine
RUN chmod +x /app/*
COPY . /app
WORKDIR /app
cmd ["npm", "start"]