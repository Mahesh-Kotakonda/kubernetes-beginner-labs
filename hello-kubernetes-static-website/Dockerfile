# Stage 1: The Build/Preparation Stage (though minimal for static content)
FROM alpine AS builder
# Create a directory to hold the static files
RUN mkdir /app
# Copy the static HTML file into the directory
COPY index.html /app/

# Stage 2: The Final Image (using a light Nginx image)
FROM nginx:alpine
# Remove the default Nginx index.html
RUN rm -rf /usr/share/nginx/html/*
# Copy the index.html from the builder stage into the Nginx serving directory
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html

# Expose port 80 (default Nginx port)
EXPOSE 80

# Nginx starts by default when this image runs.
# The default CMD of nginx:alpine is "nginx -g 'daemon off;'"
