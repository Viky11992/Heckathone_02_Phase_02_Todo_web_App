FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make start script executable
RUN chmod +x /app/start.sh

# Expose port (will be set by Railway)
EXPOSE $PORT

# Run the start script which handles migrations and starts the app
CMD ["/app/start.sh"]