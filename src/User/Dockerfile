# Use the official Python image as a base
FROM python:3.9-slim

# Set a working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (if applicable, e.g., Flask default port is 5000)
EXPOSE 5001

# Set the command to run the application
CMD ["python", "app.py"]
