FROM node:22-alpine AS runner

# Export ENV to entrypoint.sh
ENV PORT=5173

# Set working directory
WORKDIR /app

# Copy the rest of the application code
COPY . .

# Install dependencies
RUN npm install

# We use entrypoint.sh to import into the front-end any env variable at runtime
COPY docker/entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]