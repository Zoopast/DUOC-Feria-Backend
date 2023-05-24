# Use an official Python runtime as the base image
FROM python:3.11.3-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libaio1 build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the "instantclient" folder
COPY instantclient instantclient

# Set the environment variables
ENV LD_LIBRARY_PATH=/app/instantclient

# Expose the app port
EXPOSE 5000

# Start the application
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=5000"]
