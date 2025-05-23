#!/bin/sh
echo "Starting entrypoint script..."
echo "Environment variable API_BASE_URL: ${API_BASE_URL}"
echo "Creating config.js file..."
cat <<EOF > /usr/share/nginx/html/url_config.js
window.CONFIG = {
  API_BASE_URL: "${API_BASE_URL}/api"
};
EOF

echo "Entrypoint script completed."
# This script creates a config.js file in the Nginx HTML directory with the API_BASE_URL environment variable.
# It then starts the Nginx server in the foreground.