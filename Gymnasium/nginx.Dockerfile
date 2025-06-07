FROM nginx:alpine

# Copy your static site
COPY ./frontend /usr/share/nginx/html

# Copy and make the entrypoint executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
