# ITAssist Broadcast Encoder - 100 (IBE-100)
# Professional Docker Container for SCTE-35 Streaming
# Multi-stage build for optimized deployment

# Build stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install TSDuck dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install TSDuck
RUN wget -O - https://tsduck.io/download/tsduck-3.34-ubuntu20.04-amd64.deb | dpkg -i - || true
RUN apt-get update && apt-get install -f -y && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Production stage
FROM python:3.9-slim as production

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libssl1.1 \
    libffi7 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install TSDuck runtime
RUN apt-get update && apt-get install -y \
    wget \
    && wget -O - https://tsduck.io/download/tsduck-3.34-ubuntu20.04-amd64.deb | dpkg -i - || true \
    && apt-get update && apt-get install -f -y \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY tsduck_gui_simplified.py .
COPY scte35_final/ ./scte35_final/
COPY README.md .
COPY LICENSE.txt .

# Create non-root user
RUN useradd -m -u 1000 ibe100 && \
    chown -R ibe100:ibe100 /app

# Switch to non-root user
USER ibe100

# Expose ports (if needed for web interface)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD tsp --version || exit 1

# Default command
CMD ["python", "tsduck_gui_simplified.py"]

# Labels for metadata
LABEL maintainer="ITAssist Broadcast Solutions <support@itassist.one>"
LABEL version="1.0.0"
LABEL description="ITAssist Broadcast Encoder - 100 (IBE-100) - Professional SCTE-35 Streaming Application"
LABEL org.opencontainers.image.title="IBE-100"
LABEL org.opencontainers.image.description="Professional SCTE-35 streaming application with TSDuck integration"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="ITAssist Broadcast Solutions"
LABEL org.opencontainers.image.url="https://itassist.one"
LABEL org.opencontainers.image.source="https://github.com/shihan84/Encoder-100"
