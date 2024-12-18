# Use an official Debian base image
FROM debian:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    GODOT_VERSION=4.3 \
    GODOT_EXPORT_TEMPLATE=https://downloads.tuxfamily.org/godotengine/4.3/Godot_v4.3-stable_export_templates.tpz

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download Godot headless binary
RUN wget https://downloads.tuxfamily.org/godotengine/4.3/Godot_v4.3-stable_linux.x86_64.zip -O /usr/local/bin/godot && \
    chmod +x /usr/local/bin/godot

# Add Godot export templates
RUN mkdir -p /root/.local/share/godot/templates/4.3 && \
    wget $GODOT_EXPORT_TEMPLATE -O /tmp/templates.tpz && \
    unzip /tmp/templates.tpz -d /root/.local/share/godot/templates/4.0 && \
    rm /tmp/templates.tpz

# Set up work directory
WORKDIR /app

# Copy project files
COPY . .

# Export the Godot project for Web (HTML5)
RUN godot --headless --export "HTML5" /app/export/index.html

# Install a lightweight HTTP server
RUN pip install --no-cache-dir http-server

# Expose the default HTTP server port
EXPOSE 6970

# Start HTTP server to serve the web app
CMD ["http-server", "export", "-p", "6970"]