# Stage 1: Build the Vite app
FROM node:22 AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the app for production
RUN npm run build

# Stage 2: Serve the app
FROM node:22-alpine AS runner

# Set working directory
WORKDIR /app

# Copy the production build from the builder stage
COPY --from=builder /app/dist ./dist

# Install http-server globally
RUN npm install -g http-server

# Serve the app
CMD ["http-server", "dist", "-p", "5173"]