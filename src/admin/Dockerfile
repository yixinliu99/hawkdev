# Base image for MongoDB
FROM python:3.12-slim

# Install Python and related tools
RUN apt-get update

# Set up a working directory
WORKDIR /admin

# Copy application files (Python scripts, requirements, etc.) into the container
COPY . /admin

# Install Python dependencies if a requirements.txt file exists
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mongomock

