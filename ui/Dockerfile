FROM node:22 AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

RUN npm install

COPY . .

FROM node:22 AS dev

WORKDIR /app

COPY --from=builder /app .

# This is tricky!
CMD ["npm", "run", "dev", "--", "--host"]


FROM node:22-alpine AS prod

WORKDIR /app

COPY --from=builder /app .

# Accept build arg for API URL
ARG VITE_SERVER_API_URL
ENV VITE_SERVER_API_URL=$VITE_SERVER_API_URL

# Use .env.prod to overrride .env
RUN npm run build -- --mode prod 

# Install serve to host the built files
RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "5173"]