# Use Python 3.10-slim base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies file
COPY requirements.txt .

# Upgrade pip to avoid compatibility issues
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Copy project files to the container
COPY . .

# Expose port 8000 and set the command to start the server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
