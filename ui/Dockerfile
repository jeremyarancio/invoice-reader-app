FROM node:22 AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

RUN npm install --legacy-peer-deps

COPY . .

RUN npm run build

FROM node:22 AS dev

WORKDIR /app

COPY --from=builder /app .

# This is tricky!
CMD ["npm", "run", "dev", "--", "--host"]


FROM node:22-alpine AS prod

WORKDIR /app

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/dist ./dist

RUN npm install -g serve

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]