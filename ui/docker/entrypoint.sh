#!/bin/sh
set -e

npm run build

# Install http-server globally
npm install -g http-server

# Start the http-server
http-server dist -p ${PORT}