# Base image
FROM ubuntu:latest

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    gnupg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update \
    && apt-get install -y google-cloud-sdk

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Create virtual environment
RUN python3 -m venv /opt/venv

# Activate virtual environment and install requirements
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set PATH so that the venv is used by default
ENV PATH="/opt/venv/bin:$PATH"

# Default command (adjust as needed)
CMD ["python3", "-m", "scripts.fetch_sensors"]
