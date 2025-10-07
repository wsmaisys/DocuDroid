# ========================
# STAGE 1: Builder
# Uses python:3.11-slim-bullseye for dependencies installation.
# ========================
FROM python:3.11-slim-bullseye as builder

# Set working directory and common environment variables
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install *only* essential build dependencies and clean up in one step
# 'curl' is not needed in the builder stage.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    # Add any other required build libs like libpq-dev, etc. here if needed
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt constraints.txt ./

# Install dependencies into a virtual environment
RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
    && find /opt/venv -type d -name "__pycache__" -exec rm -r {} + \
    && find /opt/venv -type d -name "tests" -exec rm -r {} + \
    && find /opt/venv -type d -name "test" -exec rm -r {} + \
    && find /opt/venv -type f -name "*.pyc" -delete \
    && find /opt/venv -type f -name "*.pyo" -delete \
    && find /opt/venv -type f -name "*.pyd" -delete

# ========================
# STAGE 2: Runner (The Final, Minimal Image)
# Uses the same small base image for consistency.
# ========================
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Set environment variables for runtime
ENV PORT=8080

# Copy virtual environment from builder. This contains ONLY the Python dependencies.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install essential runtime dependencies, configure APT, and clean up in a single layer
RUN set -ex \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

# Copy only necessary project files
COPY api.py chat_manager.py pdfloader.py webloader.py ./
COPY static/ ./static/

# --- Security and Permissions ---
# Create a non-root user and group 'app'
RUN groupadd -r app && useradd -r -g app -s /sbin/nologin -d /app app \
    && chown -R app:app /app

# Create necessary directories for runtime with correct permissions
RUN mkdir -p /app/tmp && chown -R app:app /app/tmp

# Switch to non-root user
USER app
# --- End Security and Permissions ---


# Add healthcheck
# Cloud Run is typically deployed behind a load balancer that performs its own health check,
# but an internal check is good practice. Use the exposed PORT variable.
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/ || exit 1

# Expose the port
EXPOSE 8080

# Command to run the application (use the ENV variable for port)
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]