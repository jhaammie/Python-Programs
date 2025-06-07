# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5006 for the fast api app
EXPOSE 5006

# Run the Flask app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5006"]
