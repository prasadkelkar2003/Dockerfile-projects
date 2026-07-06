# --- Stage 1: Build and Dependency Isolation ---
FROM python:3.11-alpine AS builder

WORKDIR /app

# Install build dependencies safely
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies into a local directory to keep the final image clean
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: The Final Hardened Runtime ---
FROM python:3.11-alpine

# Optimize Python for container environments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Surface Reduction: Install ONLY tini for signal handling (no build tools)
RUN apk add --no-cache tini

# 2. Non-Root Security: Create a restricted system user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy dependencies and application from the builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .

# Ensure the non-root user owns the application files
RUN chown -R appuser:appgroup /app /home/appuser

# Make sure Python can find the installed dependencies
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to the secure non-root user
USER appuser

# 4. Proactive Monitoring: Healthcheck to ensure the container is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)" || exit 1

# 3. PID 1 Protection: Use tini as the init system via the Exec Form
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "app.py"]
