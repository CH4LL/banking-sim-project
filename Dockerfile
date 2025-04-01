# Start FROM a base image, in this case python, specific version, smaller variant
FROM python:3.13.2-slim

# Set environment variables to prevent log output buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy the requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./app /app/app
COPY ./scripts /app/scripts

# Expose the port Cloud Run expects
EXPOSE 8080

# Define default command to run on start
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 0 app.app:app