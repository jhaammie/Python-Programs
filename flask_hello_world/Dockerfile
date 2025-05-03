# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5005 for the Flask app
EXPOSE 5005

# Set the environment variable for Flask
ENV FLASK_APP=main.py

# Run the Flask app using Python
CMD ["python", "main.py"]
