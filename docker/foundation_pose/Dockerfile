# FoundationPose Wrapper Dockerfile
# Wraps the official FoundationPose image with an HTTP API
FROM wenbowen123/foundationpose:latest

# Set working directory
WORKDIR /app

# Install HTTP API dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    python-multipart==0.0.6

# Copy our API wrapper script into the container
COPY app.py /app/app.py

# Expose the API port
EXPOSE 5001

# Start the HTTP API server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"]