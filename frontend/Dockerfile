FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm install
RUN npm install -g vite
RUN npm run build
CMD ["vite", "preview", "--port", "5173", "--host"]
